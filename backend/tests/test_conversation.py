from backend.app.conversation import ConversationManager

def test_clarification_followup_is_combined():
    m = ConversationManager()
    cid, q = m.normalize(None, 'Show best customers')
    assert q == 'Show best customers'
    m.remember_clarification(cid, q, 'What does best mean?')
    cid2, combined = m.normalize(cid, 'By number of sites')
    assert cid2 == cid
    assert 'Show best customers' in combined
    assert 'By number of sites' in combined


def test_context_survives_retry_and_success_replaces_pending():
    m = ConversationManager()
    m.remember_clarification('a', 'Show guards', 'Which site?')
    assert m.normalize('a', 'London') == m.normalize('a', 'London')
    m.remember_result('a', 'London', {'question': 'Show guards at London', 'status': 'ok'})
    assert m.context('a')['pending_clarification'] is None
    assert m.context('a')['recent_turns'][0]['resolved_question'] == 'Show guards at London'
    assert m.context('b') == {}


def test_context_is_bounded_copied_and_expires(monkeypatch):
    from backend.app import conversation
    clock = [0]
    monkeypatch.setattr(conversation, 'monotonic', lambda: clock[0])
    m = ConversationManager(ttl=10, max_conversations=2, max_turns=2)
    for i in range(4):
        m.remember_result('a', str(i), {'question': str(i), 'result_rows': [{'id': j} for j in range(20)]})
    context = m.context('a')
    assert len(context['recent_turns']) == 2
    assert len(context['recent_turns'][0]['result_rows']) == 10
    assert context['recent_turns'][0]['results_truncated']
    context['recent_turns'].clear()
    assert len(m.context('a')['recent_turns']) == 2
    clock[0] = 11
    assert m.context('a') == {}
    for cid in ('a', 'b', 'c'):
        clock[0] += 1
        m.remember_result(cid, 'hello', {})
    assert m.context('a') == {}


def test_large_result_preview_is_omitted():
    import json
    m = ConversationManager()
    m.remember_result('a', 'Show records', {'result_rows': [{'value': 'x' * 30000}]})
    context = m.context('a')
    assert len(json.dumps(context)) < 21000
    assert context['recent_turns'][0]['results_truncated']
