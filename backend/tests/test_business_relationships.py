from types import SimpleNamespace

from backend.app import catalog
from backend.app.nodes import plan, retrieve


def test_restricted_relationships_are_documented_but_not_exposed():
    stored = catalog.static_catalog()['relationships']
    assert any(r['to_table'] == 'roles' for r in stored)
    assert any(r['from_table'] == 'client_ai_conversations' for r in stored)
    runtime = catalog.live_or_static_catalog()['relationships']
    assert len(runtime) == len(stored) - 2
    assert not any('roles' in (r['from_table'], r['to_table']) or
                   'client_ai_conversations' in (r['from_table'], r['to_table']) for r in runtime)


def test_blocked_or_missing_columns_remove_relationships():
    data = {'tables': {'a': {'columns': {'id': ''}}, 'b': {'columns': {'id': ''}}},
            'relationships': [{'from_table': 'a', 'from_column': 'secret', 'to_table': 'b', 'to_column': 'id'},
                              {'from_table': 'a', 'from_column': 'id', 'to_table': 'absent', 'to_column': 'id'}]}
    assert catalog.project_relationships(data)['relationships'] == []


def test_planner_receives_verified_relationships(monkeypatch):
    def chat(model, system, user):
        assert '"verified_by":"business_schema"' in user or '"verified_by": "business_schema"' in user
        assert 'customer_id' in user
        assert '"from_table":"sites"' in user or '"from_table": "sites"' in user
        return model(objective='Customer sites', retrieval_query='Customer sites', tables=['customers', 'sites'])
    monkeypatch.setattr(plan, 'structured_chat', chat)
    context = retrieve.retrieve_context({'question': 'Customer sites', 'intent': {'confidence': 1, 'required_tables': ['customers', 'sites']}})
    assert plan.make_plan({'question': 'Customer sites', **context})['plan']['tables'] == ['customers', 'sites']


def test_retrieval_preserves_four_table_plan_and_relevant_joins(monkeypatch):
    monkeypatch.setattr(retrieve.settings, 'top_tables', 5)
    monkeypatch.setattr(retrieve, 'get_store', lambda: SimpleNamespace(retrieve=lambda *args: {'tables': [], 'examples': []}))
    monkeypatch.setattr(retrieve.settings, 'enable_data_sampling', False)
    required = ['shift_assignments', 'shifts', 'guards', 'sites']
    result = retrieve.retrieve_context({'question': 'Assignments', 'plan': {'tables': required}})
    assert result['retrieved_tables'] == required
    relations = result['schema_context']['verified_relationships']
    assert relations
    assert all(r['from_table'] in required and r['to_table'] in required for r in relations)
    assert any(r['from_table'] == 'shift_assignments' and r['to_table'] == 'guards' for r in relations)
