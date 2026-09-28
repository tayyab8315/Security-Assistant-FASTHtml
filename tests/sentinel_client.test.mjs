import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {randomUUID} from 'node:crypto';

// Test browser logic without controlling or depending on an installed browser.
function fixture() {
  const elements=new Map(), listeners=new Map(), saved=new Map(), requests=[];
  function element(){return {innerHTML:'',textContent:'',value:'',hidden:false,disabled:false,style:{},dataset:{},scrollHeight:68,open:false,classList:{add(){},remove(){},toggle(){}},querySelectorAll(){return []},querySelector(){return element()},addEventListener(){},focus(){},setSelectionRange(){},scrollIntoView(){},showModal(){this.open=true},close(){this.open=false}};}
  for(const id of ['toast','history-search','history','page-label','welcome','conversation','library','data-view','composer-area','question','prompt-cards','conversation-title','messages','thinking','thinking-title','thinking-detail','chat-bottom','elapsed','char-count','send-button','stop-button','health-pill','health-label','modal','modal-content','ask-form','rename-title'])elements.set('#'+id,element());
  elements.set('.workspace-nav',element());
  const policy=JSON.parse(readFileSync(new URL('../backend/domain/security_policy.json',import.meta.url),'utf8'));
  const catalog=JSON.parse(readFileSync(new URL('../backend/admin/schema_catalog.json',import.meta.url),'utf8'));
  elements.get('#data-view').dataset.domains=JSON.stringify(policy.allowed_tables.filter(t=>!policy.blocked_tables.includes(t)).map(table=>({table,description:catalog.tables[table].description})));
  const document={querySelector:s=>elements.get(s)||null,querySelectorAll:()=>[],documentElement:{dataset:{}},body:element(),addEventListener:(name,fn)=>listeners.set(name,fn)};
  let result={status:'ok',conversation_id:'context-1',answer:'Three guards.'};
  const context=vm.createContext({document,localStorage:{getItem:k=>saved.get(k)||null,setItem:(k,v)=>saved.set(k,v),removeItem:k=>saved.delete(k)},crypto:{randomUUID},AbortController,console,Date,Map,JSON,setInterval:()=>1,clearInterval(){},setTimeout:()=>1,clearTimeout(){},fetch:async(url,options)=>{
    if(url==='/health')return {ok:true,json:async()=>({status:'ok',model:'fixture',dialect:'mysql'})};
    if(url.startsWith('/ask/progress/'))return {ok:true,json:async()=>({title:'Understanding your question',detail:'Identifying the information you need.'})};
    assert.equal(url,'/ask');requests.push(JSON.parse(options.body));
    return {ok:result.status!=='error',status:result.status==='error'?500:200,json:async()=>result};
  }});
  const source=readFileSync(new URL('../static/sentinel/app.js',import.meta.url),'utf8');
  const api=vm.runInContext(source+'\n({ask,newChat,renderTable,renderLibrary,renderData,renderMarkdown,tableState,getChats:()=>chats,getPrompts:()=>prompts,getPreferences:()=>preferences})',context);
  return {api,elements,listeners,saved,requests,context,respond:r=>{result=r},element};
}

test('chat, clarification IDs, HTTP errors, history and escaping',async()=>{
  const f=fixture(), {api,elements}=f;
  f.respond({status:'clarification_required',conversation_id:'clarify-1',clarification_question:'Which site?'});
  await api.ask('Show guards');assert.match(elements.get('#messages').innerHTML,/Which site\?/);
  f.respond({status:'ok',conversation_id:'clarify-1',answer:'<script>alert(1)</script>',sql:'SELECT name FROM guards'});
  await api.ask('London');assert.equal(f.requests[1].conversation_id,'clarify-1');
  assert.match(elements.get('#messages').innerHTML,/&lt;script&gt;/);assert.doesNotMatch(elements.get('#messages').innerHTML,/<script>alert/);
  assert.match(elements.get('#messages').innerHTML,/View generated SQL/);
  f.listeners.get('change')({target:{id:'technical-details-setting',checked:false}});
  assert.doesNotMatch(elements.get('#messages').innerHTML,/View generated SQL/);
  assert.equal(api.getPreferences().showTechnicalDetails,false);
  f.respond({status:'error',conversation_id:'clarify-1',answer:'Could not complete this request.'});
  await api.ask('Broken query');assert.match(elements.get('#messages').innerHTML,/Could not complete this request/);
  assert.match(elements.get('#messages').innerHTML,/Retry question/);assert.equal(api.getChats()[0].conversationId,'clarify-1');
  assert.ok(f.saved.has('sentinel.conversations.v1'));
  api.newChat();await api.ask('New topic');assert.equal(f.requests.at(-1).conversation_id,undefined);assert.equal(api.getChats().length,2);
});

test('library, data explorer, pagination, filtering and empty results',async()=>{
  const f=fixture(), {api,elements}=f;
  const domains=JSON.parse(elements.get('#data-view').dataset.domains);
  assert.equal(api.getPrompts().length,12+domains.length-4);
  api.renderLibrary();assert.equal((elements.get('#library').innerHTML.match(/class="prompt-card"/g)||[]).length,api.getPrompts().length);
  api.renderData();assert.equal((elements.get('#data-view').innerHTML.match(/class="domain-card"/g)||[]).length,domains.length);
  assert.match(elements.get('#data-view').innerHTML,/shift assignments/);
  const explore=f.element();explore.dataset.question='How many records are in shifts?';
  await f.listeners.get('click')({target:{closest:()=>explore}});
  assert.equal(elements.get('#question').value,'How many records are in shifts?');
  f.respond({status:'ok',conversation_id:'table',answer:'Records',columns:['name'],rows:Array.from({length:23},(_,i)=>({name:'Guard '+(i+1)}))});
  await api.ask('List guards');
  const message=api.getChats()[0].messages.at(-1),host=f.element();elements.set(`[data-table="${message.id}"]`,host);
  api.renderTable(message.id);assert.match(host.innerHTML,/Page 1 of 3/);assert.equal((host.innerHTML.match(/<td /g)||[]).length,10);
  f.listeners.get('change')({target:{id:'technical-details-setting',checked:false}});
  assert.doesNotMatch(elements.get('#messages').innerHTML,/result-panel/);
  assert.equal(api.getPreferences().showTechnicalDetails,false);
  api.tableState.set(message.id,{filter:'Guard 23',page:0});api.renderTable(message.id);assert.equal((host.innerHTML.match(/<td /g)||[]).length,1);
  api.tableState.set(message.id,{filter:'not found',page:0});api.renderTable(message.id);assert.match(host.innerHTML,/No rows match/);
});

test('assistant markdown renders safely',()=>{
  const {api}=fixture();
  const html=api.renderMarkdown('## Capabilities\n\n| Name | Use |\n| --- | --- |\n| **Triage** | Review alerts |\n\n- Read-only\n- `safe`\n\n<script>alert(1)</script>');
  assert.match(html,/<h2>Capabilities<\/h2>/);
  assert.match(html,/class="markdown-table"/);
  assert.match(html,/<strong>Triage<\/strong>/);
  assert.match(html,/<code>safe<\/code>/);
  assert.match(html,/&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.doesNotMatch(html,/<script>alert/);
});

test('settings, theme and browser-history preferences',async()=>{
  const f=fixture(),click=action=>f.listeners.get('click')({target:{closest:()=>({disabled:false,dataset:{action}})}});
  await click('theme');assert.equal(f.context.document.documentElement.dataset.theme,'light');
  await click('settings');assert.match(f.elements.get('#modal-content').innerHTML,/Remember conversations/);assert.equal(f.elements.get('#modal').open,true);
  f.listeners.get('change')({target:{id:'remember-setting',checked:false}});assert.equal(f.saved.has('sentinel.conversations.v1'),false);
  await click('close-modal');assert.equal(f.elements.get('#modal').open,false);
  await click('data');assert.equal(f.elements.get('#data-view').hidden,false);
  await click('chat');assert.equal(f.elements.get('#composer-area').hidden,false);
});
