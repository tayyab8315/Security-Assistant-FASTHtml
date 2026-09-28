from __future__ import annotations
from fasthtml.common import FastHTML, JSONResponse
from .config import ROOT
from starlette.requests import Request
from starlette.concurrency import run_in_threadpool
from pydantic import ValidationError
from .graph import graph
from .models import AskRequest, AskResponse
from .config import settings
from .conversation import manager
from .tracing import get_progress, request_trace, traced_step

app = FastHTML(default_hdrs=False, secret_key=settings.session_secret or None, key_fname=str(ROOT.parent / ".sesskey"))

@app.route('/health', methods=['GET'])
def health(): return JSONResponse({'status':'ok','dialect':settings.sql_dialect,'model':settings.ollama_llm_model})

def ask(request:AskRequest):
    with request_trace(request.request_id) as trace:
        response = _ask(request)
        trace.status = response.status
        return response


@app.route('/ask', methods=['POST'])
async def ask_endpoint(req: Request):
    try:
        payload = AskRequest.model_validate(await req.json())
    except (ValidationError, ValueError, TypeError):
        return JSONResponse({'detail': 'Provide a question of 1–4000 characters and an optional conversation_id (up to 120 characters).'}, status_code=422)
    result = await run_in_threadpool(ask, payload)
    return JSONResponse(result.model_dump(mode='json'), status_code=500 if result.status == 'error' else 200)


@app.route('/ask/progress/{request_id}', methods=['GET'])
def ask_progress(request_id: str):
    progress = get_progress(request_id)
    if progress is None:
        return JSONResponse({'title': 'Starting your request', 'detail': 'Connecting to the assistant.', 'complete': False})
    return JSONResponse(progress)


def _ask(request:AskRequest):
    cid, resolved_input = traced_step("Resolve conversation context", "No")(manager.normalize)(request.conversation_id, request.question)
    try: state=graph.invoke({'question':request.question,'conversation_context':manager.context(cid),'conversation_id':cid,'repair_attempts':0})
    except Exception as exc: return AskResponse(status='error',conversation_id=cid,answer=f'Pipeline error: {str(exc)[:1200]}')
    intent=state.get('intent',{})
    if state.get('status')=='clarification_required' or intent.get('needs_clarification'):
        cq=state.get('clarification_question') or intent.get('clarification_question') or 'Please clarify your request.'
        manager.remember_clarification(cid, request.question, cq, intent=intent, message=request.question)
        return AskResponse(status='clarification_required',conversation_id=cid,clarification_question=cq,debug=_debug(state))
    if state.get('status') != 'error' and (state.get('status') == 'ok' or intent.get('intent') in ('knowledge_query', 'out_of_scope', 'general_chat', 'unsafe_request')):
        manager.remember_result(cid, request.question, state)
    if intent.get('intent') == 'knowledge_query':
        return AskResponse(status='knowledge_not_found',conversation_id=cid,answer=state.get('answer'),debug=_debug(state))
    if intent.get('intent') in ('out_of_scope','general_chat'):
        return AskResponse(status='out_of_scope',conversation_id=cid,answer=state.get('answer'),debug=_debug(state))
    if intent.get('intent')=='unsafe_request':
        return AskResponse(status='unsafe_request',conversation_id=cid,answer=state.get('answer'),debug=_debug(state))
    if state.get('status')!='ok':
        return AskResponse(status='error',conversation_id=cid,answer=state.get('error','The request could not be completed safely.'),retrieved_tables=state.get('retrieved_tables',[]),debug=_debug(state))
    return AskResponse(status='ok',conversation_id=cid,answer=state.get('answer'),sql=state.get('selected_sql'),columns=state.get('result_columns',[]),rows=state.get('result_rows',[]),retrieved_tables=state.get('retrieved_tables',[]),debug=_debug(state))

def _debug(state):
    if not settings.return_debug: return None
    return {'intent':state.get('intent'),'plan':state.get('plan'),'samples':state.get('sampled_values'),'examples':state.get('examples'),'candidates':state.get('candidates'),'resolved_entities':state.get('resolved_entities',[]),'entity_resolution_status':state.get('entity_resolution_status'),'entity_resolution_ambiguities':state.get('entity_resolution_ambiguities',[]),'repair_attempts':state.get('repair_attempts',0)}


from .web_ui import register_ui

register_ui(app)
