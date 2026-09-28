from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
import importlib

import pytest

from backend.app import llm, main
from backend.app.models import AskRequest, GeneratedSQL
from backend.app.tracing import model_call, request_trace, traced_step


def test_graph_steps_and_calls_reach_request_summary(monkeypatch, capsys):
    graph_module = importlib.import_module("backend.app.graph")

    def analyze_intent(state):
        with model_call("LLM", "intent"):
            return {
                "intent": {
                    "intent": "database_query",
                    "needs_clarification": True,
                    "task_complete": False,
                },
                "clarification_question": "Which employee?",
            }

    monkeypatch.setattr(graph_module, "analyze_intent", analyze_intent)
    monkeypatch.setattr(main, "graph", graph_module.build_graph())
    response = main.ask(AskRequest(question="Show employees"))
    log = capsys.readouterr().out
    assert response.status == "clarification_required"
    assert "Step 1: Resolve conversation context" in log
    assert "Step 2: Analyze intent" in log
    assert "Step 3: Clarify" in log
    assert "Step 4:" not in log
    assert "Status: clarification_required | Steps: 3 | LLM calls: 1 | Embedding calls: 0" in log
    assert "Total request processing time:" in log


def test_json_retry_counted_as_separate_call(monkeypatch, capsys):
    responses = iter(['not json', '{"sql":"SELECT 1"}'])
    monkeypatch.setattr(llm._client, "chat", lambda **kw: SimpleNamespace(
        message=SimpleNamespace(content=next(responses))))
    with request_trace() as trace:
        traced_step("Generate", "Yes")(lambda: llm.structured_chat(GeneratedSQL, "", ""))()
        trace.status = "ok"
    log = capsys.readouterr().out
    assert "LLM call 2 (GeneratedSQL, attempt 2)" in log
    assert "LLM call: Yes (2)" in log
    assert "LLM calls: 2" in log


def test_failed_step_still_prints_total_and_resets_context(capsys):
    @traced_step("Fail", "Yes")
    def fail():
        with model_call("LLM", "test"):
            raise RuntimeError("sensitive error text")

    with pytest.raises(RuntimeError):
        with request_trace():
            fail()
    with request_trace() as second:
        traced_step("Next", "No")(lambda: None)()
        second.status = "ok"
    log = capsys.readouterr().out
    assert "Step 1: Fail | ERROR" in log
    assert "Status: error" in log
    assert "Step 1: Next" in log
    assert "sensitive error text" not in log
    assert log.count("Total request processing time:") == 2


def test_concurrent_requests_have_independent_counts():
    def run(count):
        with request_trace() as trace:
            for _ in range(count):
                with model_call("LLM", "test"):
                    pass
            return trace.request_id, trace.llm_calls

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, [1, 3]))
    assert results[0][0] != results[1][0]
    assert [r[1] for r in results] == [1, 3]
