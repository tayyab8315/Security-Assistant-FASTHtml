from __future__ import annotations
import json
from pathlib import Path
from backend.app.graph import graph, route_intent

ROOT = Path(__file__).resolve().parents[1]


def check_case(case, state):
    route = route_intent(state)
    status = {'unsafe': 'unsafe_request', 'clarify': 'clarification_required',
              'out_of_scope': 'out_of_scope', 'general': 'out_of_scope',
              'knowledge': 'knowledge_not_found'}.get(route, state.get('status', 'error'))
    clarify_ok = (status == 'clarification_required') == bool(case.get('should_clarify', False))
    tables_ok = set(case.get('expected_tables', [])).issubset(state.get('retrieved_tables', []))
    expected_status = case.get('expected_status')
    if expected_status == 'error_or_out_of_scope':
        status_ok = status in {'error', 'out_of_scope', 'unsafe_request'}
    elif expected_status:
        status_ok = status == expected_status
    else:
        status_ok = status == ('clarification_required' if case.get('should_clarify') else 'ok')
    return clarify_ok and tables_ok and status_ok, status

if __name__ == "__main__":
    cases = json.loads((ROOT / "eval" / "cases.json").read_text())
    passed = 0
    for idx, case in enumerate(cases, 1):
        state = graph.invoke({"question": case["question"], "repair_attempts": 0})
        retrieved = set(state.get("retrieved_tables", []))
        expected = set(case.get("expected_tables", []))
        decision = state.get("intent", {}).get("intent")
        ok, actual_status = check_case(case, state)
        passed += int(ok)
        print(f"[{idx:02}] {'PASS' if ok else 'FAIL'} | {case['question']}")
        print("     retrieved=", sorted(retrieved), "intent=", decision, "status=", actual_status, "sql=", state.get("selected_sql"))
    print(f"\nPassed {passed}/{len(cases)} basic pipeline checks")
    raise SystemExit(0 if passed == len(cases) else 1)
