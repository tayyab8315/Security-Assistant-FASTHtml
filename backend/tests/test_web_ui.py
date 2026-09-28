"""HTTP and markup contracts for the Sentinel FastHTML frontend."""
from bs4 import BeautifulSoup
import pytest
from starlette.testclient import TestClient
from backend.app import main
from backend.app.models import AskResponse
import json
from backend.app.catalog import security_policy


@pytest.mark.parametrize('path', ['/', '/chat'])
def test_sentinel_shell_and_local_assets(path):
    with TestClient(main.app) as client:
        reply = client.get(path)
        assert reply.status_code == 200
        doc = BeautifulSoup(reply.text, 'html.parser')
        assert doc.html['data-theme'] == 'dark'
        assert doc.select_one('.intro h1').get_text('|', strip=True) == 'Your operations.|A conversation away.'
        assert len(doc.select('.prompt-grid .prompt-card')) == 3
        for selector in ('#sidebar', '#history-search', '#history', '#library', '#data-view', '#modal', '#toast', '#thinking', '#ask-form', '#question', '#send-button'):
            assert doc.select_one(selector) is not None
        assert doc.select_one('#send-button').has_attr('disabled')
        assert doc.select_one('#conversation').has_attr('hidden')
        assert doc.select_one('#question')['maxlength'] == '4000'
        for element, attr in [('link[rel=stylesheet]', 'href'), ('script[type=module]', 'src'), ('link[rel=icon]', 'href')]:
            asset = doc.select_one(element)[attr]
            assert asset.startswith('/static/sentinel/')
            assert client.get(asset).status_code == 200
        assert 'unpkg.com' not in reply.text
        assert 'cdn.jsdelivr.net' not in reply.text


def test_question_prefill_is_escaped():
    with TestClient(main.app) as client:
        value = '</textarea><script>alert(1)</script>'
        reply = client.get('/chat', params={'question': value})
        doc = BeautifulSoup(reply.text, 'html.parser')
        assert doc.select_one('#question').get_text() == value
        assert len(doc.select('script')) == 1
        long = client.get('/chat', params={'question': 'x' * 5000})
        assert len(BeautifulSoup(long.text, 'html.parser').select_one('#question').get_text()) == 4000


def test_data_explorer_uses_configured_allowed_tables():
    reply = TestClient(main.app).get('/')
    doc = BeautifulSoup(reply.text, 'html.parser')
    domains = json.loads(doc.select_one('#data-view')['data-domains'])
    assert {d['table'] for d in domains} == set(security_policy()['allowed_tables'])
    assert not {d['table'] for d in domains} & set(security_policy()['blocked_tables'])
    assert 'bank_account_number' not in doc.select_one('#data-view')['data-domains']


@pytest.mark.parametrize('status', ['ok', 'clarification_required', 'knowledge_not_found', 'out_of_scope', 'unsafe_request', 'error'])
def test_browser_response_contract(monkeypatch, status):
    captured = []
    def answer(request):
        captured.append(request)
        return AskResponse(status=status, conversation_id='same-context', answer='Result',
                           clarification_question='Which site?' if status == 'clarification_required' else None,
                           columns=['count'], rows=[{'count': 3}], sql='SELECT COUNT(*) FROM guards', retrieved_tables=['guards'])
    monkeypatch.setattr(main, 'ask', answer)
    with TestClient(main.app) as client:
        reply = client.post('/ask', json={'question': 'How many guards?', 'conversation_id': 'same-context'})
        assert reply.status_code == (500 if status == 'error' else 200)
        assert reply.json()['status'] == status
        assert reply.json()['conversation_id'] == 'same-context'
        assert captured[0].conversation_id == 'same-context'
        assert reply.json()['rows'] == [{'count': 3}]


def test_request_validation(monkeypatch):
    def unexpected(request):
        raise AssertionError('Invalid input must not reach the pipeline')
    monkeypatch.setattr(main, 'ask', unexpected)
    with TestClient(main.app) as client:
        for payload in ({}, {'question': ''}, {'question': ' '}, {'question': 'a' * 4001}):
            assert client.post('/ask', json=payload).status_code == 422


def test_assets_do_not_expose_project_files():
    with TestClient(main.app) as client:
        assert client.get('/static/sentinel/.env').status_code == 404
        assert client.get('/static/sentinel/%2e%2e/%2e%2e/backend/.env').status_code == 404


def test_progress_endpoint_exposes_safe_user_facing_status():
    with TestClient(main.app) as client:
        initial = client.get('/ask/progress/new-request').json()
        assert initial == {'title': 'Starting your request', 'detail': 'Connecting to the assistant.', 'complete': False}
    from backend.app.tracing import get_progress, request_trace, traced_step
    with request_trace('progress-test'):
        traced_step('Analyze intent', 'Yes')(lambda: {})()
        progress = get_progress('progress-test')
        assert progress['title'] == 'Understanding your question'
        assert progress['detail'] == 'Identifying the information you need.'
