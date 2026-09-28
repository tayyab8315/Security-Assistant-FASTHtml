import json
from copy import deepcopy
from unittest.mock import Mock

from backend.app.catalog import display_rules
from backend.app.nodes import answer


def test_only_planned_tables_reach_final_answer(monkeypatch):
    chat = Mock(return_value="One active guard.")
    monkeypatch.setattr(answer, "text_chat", chat)
    state = {
        "question": "Show guard status",
        "plan": {"tables": ["guards"]},
        "retrieved_tables": ["guards", "sites", "customers"],
        "selected_sql": "SELECT g.status AS guard_status, COUNT(*) AS n FROM guards g GROUP BY g.status LIMIT 20",
        "result_columns": ["guard_status", "n"],
        "result_rows": [{"guard_status": 1, "n": 1}],
    }
    original = deepcopy(state)
    assert answer.build_answer(state) == {"answer": "One active guard."}
    chat.assert_called_once()
    system, user = chat.call_args.args
    rules = json.loads(user.split("Approved display rules for planner-selected tables: ", 1)[1]
                       .split("\nValidated SQL", 1)[0])
    assert set(rules["tables"]) == {"guards"}
    assert rules["tables"]["guards"]["columns"]["status"]["values"]["1"] == "Active"
    assert state["selected_sql"] in user
    assert "Never apply a status mapping to a count" in system
    assert state == original


def test_rule_selection_deduplicates_and_filters_restricted_tables():
    rules = display_rules(["guards", "guard_availabilities", "guards", "roles", "unknown"])
    assert set(rules["tables"]) == {"guards", "guard_availabilities"}
    assert "license_number" not in rules["tables"]["guards"]["columns"]
    assert rules["tables"]["guard_availabilities"]["columns"]["status"]["values"]["available"] == "Available"
    assert display_rules([])["tables"] == {}


def test_missing_plan_does_not_fall_back_to_retrieved_tables(monkeypatch):
    selector = Mock(return_value={"defaults": {}, "tables": {}})
    monkeypatch.setattr(answer, "display_rules", selector)
    monkeypatch.setattr(answer, "text_chat", Mock(return_value="No matching rows were found."))
    answer.build_answer({"question": "Show records", "retrieved_tables": ["guards"]})
    selector.assert_called_once_with([])
