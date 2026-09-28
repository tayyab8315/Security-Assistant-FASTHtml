import importlib
import json
import pytest
from backend.app.nodes import plan, retrieve
from backend.app.models import QueryPlan


def test_planner_only_receives_retrieved_schema(monkeypatch):
    context = {'tables': {'guards': {'description': 'Guards', 'columns': {'id': 'Unique identifier'}}},
               'verified_relationships': [], 'business_glossary': {}}
    def chat(model, system, user):
        assert 'Unique identifier' in user
        assert 'guard_availabilities' not in user
        return QueryPlan(objective='List guards', retrieval_query='guards', tables=['guards'])
    monkeypatch.setattr(plan, 'structured_chat', chat)
    assert plan.make_plan({'question': 'List guards', 'schema_context': context})['plan']['tables'] == ['guards']
    monkeypatch.setattr(plan, 'structured_chat', lambda *a: QueryPlan(
        objective='Other', retrieval_query='other', tables=['sites']))
    with pytest.raises(ValueError, match='outside the retrieved schema'):
        plan.make_plan({'question': 'List guards', 'schema_context': context})


def test_join_bridge_and_limit(monkeypatch):
    catalog = {'tables': {t: {} for t in ['a', 'bridge', 'b']}, 'relationships': [
        {'from_table': 'a', 'to_table': 'bridge'}, {'from_table': 'bridge', 'to_table': 'b'}]}
    monkeypatch.setattr(retrieve.settings, 'top_tables', 3)
    assert set(retrieve.include_join_tables(['a', 'b'], catalog)) == {'a', 'bridge', 'b'}
    monkeypatch.setattr(retrieve.settings, 'top_tables', 2)
    with pytest.raises(ValueError, match='TOP_TABLES'):
        retrieve.include_join_tables(['a', 'b'], catalog)


def test_database_workflow_retrieves_before_planning(monkeypatch):
    service = importlib.import_module('backend.app.services.database_query')
    calls = []
    def retrieval(state):
        calls.append('retrieve')
        return {'schema_context': {'tables': {'guards': {'columns': {'id': 'ID'}}}}}
    def planning(state):
        assert calls == ['retrieve']
        assert 'guards' in state['schema_context']['tables']
        calls.append('plan')
        return {'plan': {'tables': ['guards']}}
    monkeypatch.setattr(service, 'retrieve_context', retrieval)
    monkeypatch.setattr(service, 'make_plan', planning)
    monkeypatch.setattr(service, 'generate_candidates', lambda state: {})
    monkeypatch.setattr(service, 'validate_candidates', lambda state: {'selected_sql': 'SELECT id FROM guards LIMIT 20'})
    monkeypatch.setattr(service, 'execute_query', lambda state: {'status': 'ok'})
    monkeypatch.setattr(service, 'build_answer', lambda state: {'answer': 'Done'})
    service.DatabaseQueryService().run({'question': 'List guards'})
    assert calls == ['retrieve', 'plan']
