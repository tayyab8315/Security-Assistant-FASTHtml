from unittest.mock import Mock

import pytest

from backend.app.nodes import retrieve


@pytest.fixture
def retrieval(monkeypatch):
    tables = {name: {'columns': {'id': 'ID'}} for name in ('payroll', 'guards', 'sites', 'users')}
    monkeypatch.setattr(retrieve, 'live_or_static_catalog', lambda: {'tables': tables})
    monkeypatch.setattr(retrieve.settings, 'top_tables', 3)
    monkeypatch.setattr(retrieve.settings, 'enable_data_sampling', False)
    glossary = {'rules': ['Keep security rules'], 'query_rules': {'payroll': {}, 'users': {}},
                'synonyms': [{'maps_to': 'payroll'}, {'maps_to': 'users.name'}]}
    monkeypatch.setattr(retrieve, 'business_glossary', lambda: glossary)
    examples = [{'question': 'Count payroll', 'tables': ['payroll'], 'sql': 'SELECT COUNT(*) FROM payroll'},
                {'question': 'Users', 'tables': ['users'], 'sql': 'SELECT id FROM users'}]
    monkeypatch.setattr(retrieve, 'examples', lambda: examples)
    store = Mock()
    store.retrieve.return_value = {'tables': ['users', 'sites', 'guards'], 'examples': examples}
    get_store = Mock(return_value=store)
    monkeypatch.setattr(retrieve, 'get_store', get_store)
    return get_store, glossary


def state(confidence, tables=None):
    return {'question': 'Count payroll', 'intent': {'confidence': confidence, 'required_tables': ['payroll']},
            'plan': {'tables': ['payroll'] if tables is None else tables}}


def test_confident_request_does_not_pad_schema_or_call_vector_store(retrieval):
    get_store, glossary = retrieval
    result = retrieve.retrieve_context(state(0.76))
    assert result['retrieved_tables'] == ['payroll']
    assert list(result['schema_context']['tables']) == ['payroll']
    assert list(result['schema_context']['business_glossary']['query_rules']) == ['payroll']
    assert result['schema_context']['business_glossary']['rules'] == glossary['rules']
    assert 'users' in glossary['query_rules']  # Source configuration stays intact.
    assert len(result['examples']) == 1
    get_store.assert_not_called()


@pytest.mark.parametrize('confidence', [0, 0.74, 0.75])
def test_fallback_keeps_existing_limit_and_required_table(retrieval, confidence):
    result = retrieve.retrieve_context(state(confidence))
    assert result['retrieved_tables'] == ['payroll', 'users', 'sites']
    retrieval[0].assert_called_once()


def test_planned_join_tables_survive_high_confidence_selection(retrieval):
    result = retrieve.retrieve_context(state(0.9, ['payroll', 'guards', 'sites']))
    assert result['retrieved_tables'] == ['payroll', 'guards', 'sites']
    retrieval[0].assert_not_called()


def test_intent_tables_used_when_plan_has_none(retrieval):
    assert retrieve.retrieve_context(state(0.9, []))['retrieved_tables'] == ['payroll']


def test_unknown_tables_cannot_enter_schema(retrieval):
    request = state(0.9, ['forbidden'])
    request['intent']['required_tables'] = ['forbidden']
    result = retrieve.retrieve_context(request)
    assert result['retrieved_tables'] == ['users', 'sites', 'guards']
    retrieval[0].assert_called_once()


def test_oversized_required_join_is_rejected_instead_of_truncated(retrieval):
    with pytest.raises(ValueError, match='TOP_TABLES'):
        retrieve.retrieve_context(state(0.9, ['payroll', 'guards', 'sites', 'users']))
