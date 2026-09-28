from starlette.testclient import TestClient

from backend.app import main
from backend.app.models import IntentUnderstanding
from backend.app.nodes import intent


def test_intent_receives_only_table_names_and_descriptions(monkeypatch):
    state = {"question": "Include guard license numbers", "schema_context": {
        "tables": {"guards": {"columns": {"license_expiry": "Expiry date"}}}
    }}

    def chat(model, system, user):
        import json
        directory = json.loads(user.split("Database capability:", 1)[1])
        assert set(directory) == {"tables"}
        assert directory["tables"]
        assert all(set(info) == {"description"} for info in directory["tables"].values())
        assert "roles" not in directory["tables"]
        assert '"license_number"' not in user
        assert "Never request excluded tables or blocked columns" in system
        return IntentUnderstanding(intent="out_of_scope", confidence=1.0, short_reason="Guard license numbers are restricted by the current policy.")

    monkeypatch.setattr(intent, "structured_chat", chat)
    result = intent.analyze_intent(state)
    assert result["intent"]["intent"] == "out_of_scope"
    assert result["clarification_question"] == ""
    assert "license_number" not in state["schema_context"]["tables"]["guards"]["columns"]


def test_api_returns_restriction_explanation_without_debug(monkeypatch):
    reason = "Guard license numbers are restricted by the current policy."
    monkeypatch.setattr(main.settings, "return_debug", False)
    monkeypatch.setattr(main.graph, "invoke", lambda state: {
        "intent": {"intent": "out_of_scope", "short_reason": reason}, "answer": reason
    })
    response = TestClient(main.app).post("/ask", json={"question": "Show license numbers"}).json()
    assert response["status"] == "out_of_scope"
    assert response["answer"] == reason
    assert response["clarification_question"] is None
    assert response["sql"] is None
    assert response["debug"] is None
