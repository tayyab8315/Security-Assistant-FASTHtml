import json

from backend.app.models import GeneratedSQL, QueryPlan
from backend.app.nodes import generate, plan, repair


def test_output_and_supporting_columns_reach_generation_and_repair(monkeypatch):
    state = {
        "question": "Show active guard names, sorted by ID",
        "schema_context": {"tables": {"guards": {"columns": {
            "id": "ID", "first_name": "Name", "last_name": "Surname", "status": "Status"
        }}}},
    }

    def planning(model, system, user):
        assert model is QueryPlan
        assert "supporting_columns" in system
        return QueryPlan(
            objective=state["question"], retrieval_query="guards", tables=["guards"],
            columns=["guards.first_name", "guards.last_name"],
            supporting_columns=["guards.status", "guards.id"],
            filters=["guards.status = 1"], order_by=["guards.id"],
        )

    monkeypatch.setattr(plan, "structured_chat", planning)
    state.update(plan.make_plan(state))
    calls = []

    def generation(model, system, user, **kwargs):
        supplied = json.loads(user.split("Plan: ", 1)[1].split("\n", 1)[0])
        assert supplied["columns"] == ["guards.first_name", "guards.last_name"]
        assert supplied["supporting_columns"] == ["guards.status", "guards.id"]
        assert "plan.supporting_columns are internal dependencies" in system
        calls.append(user)
        return GeneratedSQL(sql="SELECT first_name, last_name FROM guards WHERE status = 1 ORDER BY id LIMIT 20")

    monkeypatch.setattr(generate.settings, "sql_candidates", 1)
    monkeypatch.setattr(generate, "structured_chat", generation)
    monkeypatch.setattr(repair, "structured_chat", generation)
    state.update(generate.generate_candidates(state))
    repair.repair_sql(state)
    assert len(calls) == 2
