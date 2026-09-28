from __future__ import annotations
from langgraph.graph import StateGraph, START, END
from .state import Text2SQLState
from .nodes.intent import analyze_intent
from .entity_resolver import resolve_entities
from .nodes.final_responses import handle_general_chat, handle_knowledge_query, handle_out_of_scope, handle_unsafe_request
from .services.database_query import database_query_service
from .tracing import traced_step

def route_intent(state):
    intent = state.get('intent', {})
    if intent.get('intent') == 'unsafe_request': return 'unsafe'
    if intent.get('needs_clarification') or not intent.get('task_complete', True):
        return 'clarify'
    if intent.get('confidence',1) < 0.60:
        return 'clarify'
    if intent.get('intent') == 'database_query':
        if state.get('entity_resolution_status') == 'ambiguous':
            return 'clarify'
        return 'database'
    if intent.get('intent') == 'knowledge_query': return 'knowledge'
    if intent.get('intent') == 'general_chat': return 'general'
    if intent.get('intent') == 'out_of_scope': return 'out_of_scope'
    return 'out_of_scope'

def mark_clarification(state):
    return {'status':'clarification_required', 'clarification_question': state.get('clarification_question') or state.get('intent',{}).get('clarification_question') or 'Please clarify your request.'}

def build_graph():
    g=StateGraph(Text2SQLState)
    for name,node,llm in [('analyze_intent',analyze_intent,'Yes'),('resolve_entities',resolve_entities,'No'),('clarify',mark_clarification,'No'),('knowledge',handle_knowledge_query,'Yes'),('general',handle_general_chat,'Yes'),('out_of_scope',handle_out_of_scope,'Yes'),('unsafe',handle_unsafe_request,'Yes')]: g.add_node(name, traced_step(name.replace('_', ' ').capitalize(), llm)(node))
    g.add_node('database', database_query_service.run)
    g.add_edge(START,'analyze_intent')
    g.add_conditional_edges('analyze_intent',lambda state: 'resolve' if (state.get('intent',{}).get('intent') == 'database_query' and not state.get('intent',{}).get('needs_clarification') and state.get('intent',{}).get('task_complete', True) and state.get('intent',{}).get('confidence', 1) >= 0.60) else route_intent(state), {'resolve':'resolve_entities','clarify':'clarify','database':'database','knowledge':'knowledge','general':'general','out_of_scope':'out_of_scope','unsafe':'unsafe'})
    g.add_conditional_edges('resolve_entities',route_intent,{'clarify':'clarify','database':'database','knowledge':'knowledge','general':'general','out_of_scope':'out_of_scope','unsafe':'unsafe'})
    g.add_edge('clarify',END)
    g.add_edge('knowledge',END)
    g.add_edge('general',END)
    g.add_edge('out_of_scope',END)
    g.add_edge('unsafe',END)
    g.add_edge('database',END)
    return g.compile()

graph=build_graph()
