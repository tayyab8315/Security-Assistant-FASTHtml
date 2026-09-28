from unittest.mock import Mock
import pytest
from backend.app import main
from backend.app.conversation import ConversationManager
from backend.app.models import AskRequest, IntentUnderstanding
from backend.app.nodes import intent


@pytest.mark.parametrize('resolved', ['Show London guards who worked yesterday', 'Count all sites'])
def test_intent_publishes_standalone_question(monkeypatch, resolved):
    monkeypatch.setattr(intent, 'live_or_static_catalog', lambda: {'tables': {}})
    model = Mock(return_value=IntentUnderstanding(intent='database_query', confidence=1, resolved_question=resolved))
    monkeypatch.setattr(intent, 'structured_chat', model)
    context = {'recent_turns': [{'resolved_question': 'Show London guards'}]}
    result = intent.analyze_intent({'question': 'latest message', 'conversation_context': context})
    assert result['question'] == resolved
    assert 'Show London guards' in model.call_args.args[2]
    assert 'latest message' in model.call_args.args[2]


def test_unresolved_context_requires_clarification(monkeypatch):
    monkeypatch.setattr(intent, 'live_or_static_catalog', lambda: {'tables': {}})
    monkeypatch.setattr(intent, 'structured_chat', lambda *a: IntentUnderstanding(intent='database_query', confidence=1))
    result = intent.analyze_intent({'question': 'those', 'conversation_context': {'recent_turns': [{}]}})
    assert result['intent']['needs_clarification']


def test_request_lifecycle_preserves_context_on_error(monkeypatch):
    manager = ConversationManager()
    monkeypatch.setattr(main, 'manager', manager)
    graph = Mock()
    monkeypatch.setattr(main, 'graph', graph)
    graph.invoke.return_value = {'status': 'ok', 'question': 'Show London guards',
                                'intent': {'intent': 'database_query'}, 'result_rows': [{'id': 7}]}
    reply = main._ask(AskRequest(question='Show London guards'))
    cid = reply.conversation_id
    graph.invoke.side_effect = RuntimeError('temporary failure')
    manager.remember_clarification(cid, 'Show London guards', 'Which date?')
    assert main._ask(AskRequest(question='Yesterday', conversation_id=cid)).status == 'error'
    sent = graph.invoke.call_args.args[0]
    assert sent['question'] == 'Yesterday'
    assert sent['conversation_context']['recent_turns'][0]['result_rows'] == [{'id': 7}]
    assert manager.context(cid)['pending_clarification']
    graph.invoke.side_effect = None
    graph.invoke.return_value = {'status': 'ok', 'question': 'Show London guards who worked yesterday',
                                'intent': {'intent': 'database_query'}}
    main._ask(AskRequest(question='Yesterday', conversation_id=cid))
    assert manager.context(cid)['pending_clarification'] is None


def test_graph_passes_resolved_question_to_database(monkeypatch):
    from backend.app import graph as graph_module
    monkeypatch.setattr(intent, 'live_or_static_catalog', lambda: {'tables': {}})
    monkeypatch.setattr(intent, 'structured_chat', lambda *a: IntentUnderstanding(
        intent='database_query', confidence=1, resolved_question='Show London guards who worked yesterday'))
    monkeypatch.setattr(graph_module, 'resolve_entities', lambda state: {})
    database = Mock(return_value={'status': 'ok'})
    monkeypatch.setattr(graph_module.database_query_service, 'run', database)
    graph_module.build_graph().invoke({'question': 'Which worked yesterday?',
                                      'conversation_context': {'recent_turns': [{'resolved_question': 'Show London guards'}]}})
    assert database.call_args.args[0]['question'] == 'Show London guards who worked yesterday'


def test_missing_reference_routes_to_clarification(monkeypatch):
    from backend.app.graph import route_intent
    monkeypatch.setattr(intent, 'live_or_static_catalog', lambda: {'tables': {}})
    monkeypatch.setattr(intent, 'structured_chat', lambda *a: IntentUnderstanding(
        intent='database_query', confidence=1, missing_required_context=True,
        resolved_question='Show details for the second guard'))
    result = intent.analyze_intent({'question': 'Show details for the second guard'})
    assert route_intent(result) == 'clarify'


def test_partial_name_reply_preserves_request_and_one_intent_call(monkeypatch):
    manager = ConversationManager()
    monkeypatch.setattr(main, 'manager', manager)
    monkeypatch.setattr(intent, 'live_or_static_catalog', lambda: {'tables': {}})
    original = 'tell me ashfaque is available to work tonight after 10PM ?'
    manager.remember_clarification('partial', original,
        "Which date, and is Ashfaque the first or last name?",
        intent={'known_details': ['Guard named Ashfaque', 'Availability after 10 PM'],
                'missing_information': ['date', 'name field']})
    model = Mock(return_value=IntentUnderstanding(
        intent='database_query', confidence=1, needs_clarification=True,
        task_complete=False, clarification_question='Which date should I check?',
        resolved_question='Check whether guard first name Ashfaque is available after 10 PM on the intended date.',
        known_details=['Guard first name is Ashfaque', 'Availability after 10 PM'],
        missing_information=['date']))
    monkeypatch.setattr(intent, 'structured_chat', model)
    graph = Mock()
    graph.invoke.side_effect = intent.analyze_intent
    monkeypatch.setattr(main, 'graph', graph)
    response = main._ask(AskRequest(question='1st name', conversation_id='partial'))
    assert response.clarification_question == 'Which date should I check?'
    model.assert_called_once()
    prompt = model.call_args.args[2]
    assert original in prompt and '1st name' in prompt
    assert prompt.index('pending_clarification') < prompt.index('Database capability:')
    pending = manager.context('partial')['pending_clarification']
    assert pending['original_question'] == original
    assert pending['known_details'] == ['Guard first name is Ashfaque', 'Availability after 10 PM']
    assert pending['unresolved_questions'] == ['date']
    assert pending['exchanges'][0]['reply'] == '1st name'
    # A second partial reply retains the prior answer even if model fields are absent.
    manager.remember_clarification('partial', 'Friday', 'Which Friday?', message='Friday')
    pending = manager.context('partial')['pending_clarification']
    assert [e['reply'] for e in pending['exchanges']] == ['1st name', 'Friday']
    assert 'Guard first name is Ashfaque' in pending['known_details']
    assert pending['original_question'] == original


def test_new_topic_replaces_pending_task():
    manager = ConversationManager()
    manager.remember_clarification('a', 'Check guard availability', 'Which date?')
    manager.remember_clarification('a', 'Show invoices', 'Which customer?',
                                   intent={'clarification_relation': 'new_request'}, message='Show invoices')
    pending = manager.context('a')['pending_clarification']
    assert pending['original_question'] == 'Show invoices'
    assert pending['exchanges'] == []


def test_temporal_context_uses_business_zone_without_assuming_server_zone(monkeypatch):
    from datetime import datetime, timezone
    class Clock:
        @staticmethod
        def now(tz):
            return datetime(2026, 9, 25, 22, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(intent, 'datetime', Clock)
    monkeypatch.setattr(intent.settings, 'business_timezone', 'Asia/Karachi')
    assert intent.temporal_context()['current_date'] == '2026-09-26'
    assert intent.temporal_context()['current_weekday'] == 'Saturday'
    monkeypatch.setattr(intent.settings, 'business_timezone', '')
    assert intent.temporal_context()['business_timezone'] is None
    assert 'current_date' not in intent.temporal_context()


@pytest.mark.parametrize('with_timezone_issue', [False, True])
def test_name_lookup_is_deferred_but_other_context_is_retained(monkeypatch, with_timezone_issue):
    from backend.app.models import ClarificationItem
    monkeypatch.setattr(intent, 'live_or_static_catalog', lambda: {'tables': {}})
    items = [ClarificationItem(kind='entity_reference', question='First or last name?')]
    if with_timezone_issue:
        items.append(ClarificationItem(kind='required_context', question='Which timezone?'))
    model = Mock(return_value=IntentUnderstanding(
        intent='database_query', confidence=.9, entity_values=['Ashfaque'],
        needs_clarification=True, task_complete=False, clarification_items=items))
    monkeypatch.setattr(intent, 'structured_chat', model)
    monkeypatch.setattr(intent.settings, 'enable_entity_resolution', True)
    original = 'tell me ashfaque is available to work tonight after 10PM ?'
    result = intent.analyze_intent({'question': original})
    assert result['intent']['needs_clarification'] == with_timezone_issue
    assert result['clarification_question'] == ('Which timezone?' if with_timezone_issue else '')
    assert result['intent']['resolved_question'] == original
    model.assert_called_once()


def test_literal_values_reach_resolver_without_keyword_patterns():
    from backend.app.entity_resolver import _extract_entity_texts
    values = _extract_entity_texts('tell me ashfaque is available tonight',
                                   {'entity_values': ['Ashfaque']}, {'tables': {}})
    assert 'Ashfaque' in values
