from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

from backend.app import llm, main
from backend.app.catalog import prompt
from backend.app.tracing import request_trace
from backend.app.models import AskRequest, AskResponse, GeneratedSQL


def response(content, thinking=None):
    return SimpleNamespace(message=SimpleNamespace(content=content, thinking=thinking), done_reason="stop")


def test_structured_instruction_has_real_newlines():
    text = prompt("structured_output_instruction", schema="{}")
    assert text.startswith("\nReturn")
    assert "schema:\n{}" in text
    assert "\\n" not in text


@pytest.mark.parametrize("empty", [None, "", "   "])
def test_empty_content_retries_without_using_thinking(monkeypatch, empty):
    client = Mock()
    client.chat.side_effect = [response(empty, '{"sql":"SELECT forbidden FROM secrets"}'), response('{"sql":"SELECT 1"}')]
    monkeypatch.setattr(llm, "_client", client)
    assert llm.structured_chat(GeneratedSQL, "system", "user").sql == "SELECT 1"
    assert client.chat.call_count == 2
    assert all(m["role"] != "assistant" for m in client.chat.call_args.kwargs["messages"])


def test_thinking_only_output_fails_without_leaking(monkeypatch, capsys):
    client = Mock()
    client.chat.return_value = response("", '{"sql":"PRIVATE_THINKING"}')
    monkeypatch.setattr(llm, "_client", client)
    with request_trace():
        with pytest.raises(ValueError, match="after two attempts"):
            llm.structured_chat(GeneratedSQL, "system", "user")
    assert client.chat.call_count == 2
    assert "PRIVATE_THINKING" not in capsys.readouterr().out


def test_text_answer_retries_empty_response(monkeypatch):
    client = Mock()
    client.chat.side_effect = [response(None), response("There are 3 guards.")]
    monkeypatch.setattr(llm, "_client", client)
    assert llm.text_chat("system", "user") == "There are 3 guards."
    assert client.chat.call_count == 2


def test_text_answer_does_not_succeed_with_empty_content(monkeypatch):
    client = Mock()
    client.chat.return_value = response(" ", "private reasoning")
    monkeypatch.setattr(llm, "_client", client)
    with pytest.raises(ValueError, match="empty final answer"):
        llm.text_chat("system", "user")
    assert client.chat.call_count == 2


@pytest.mark.parametrize("status, expected_http", [("error", 500), ("ok", 200), ("clarification_required", 200)])
def test_http_status_preserves_response_body_and_direct_call(monkeypatch, status, expected_http):
    result = AskResponse(status=status, conversation_id="test", answer="test")
    monkeypatch.setattr(main, "_ask", lambda request: result)
    assert main.ask(AskRequest(question="hello")) == result
    with TestClient(main.app) as client:
        reply = client.post("/ask", json={"question":"hello"})
    assert reply.status_code == expected_http
    assert reply.json()["status"] == status


def test_database_graph_completes_with_stubbed_external_services(monkeypatch):
    import json
    from backend.app import catalog
    from backend.app.nodes import execute, generate, retrieve, validate

    monkeypatch.setattr(catalog, "inspect_live_schema", Mock(side_effect=RuntimeError("offline test")))
    store = Mock()
    store.retrieve.return_value = {"tables": ["guards"], "examples": []}
    monkeypatch.setattr(retrieve, "get_store", lambda: store)
    monkeypatch.setattr(retrieve, "sample_distinct", lambda *args: [])
    monkeypatch.setattr(validate, "explain", lambda sql: None)
    monkeypatch.setattr(execute, "execute_select", lambda sql: (["guard_count"], [{"guard_count": 3}]))
    monkeypatch.setattr(generate.settings, "sql_candidates", 3)
    outputs = [
        {"intent": "database_query", "confidence": 1.0, "required_tables": ["guards"]},
        {"objective": "Count guards", "retrieval_query": "guards count", "tables": ["guards"]},
        *[{"sql": "SELECT COUNT(*) AS guard_count FROM guards"}] * 3,
    ]
    client = Mock()
    client.chat.side_effect = [response(json.dumps(value)) for value in outputs] + [response("There are 3 guards.")]
    monkeypatch.setattr(llm, "_client", client)
    with TestClient(main.app) as api:
        result = api.post("/ask", json={"question": "How many guards are in the system?"})
    assert result.status_code == 200
    assert result.json()["status"] == "ok"
    assert result.json()["rows"] == [{"guard_count": 3}]
    assert result.json()["answer"] == "There are 3 guards."
    assert client.chat.call_count == 6
