from __future__ import annotations
from collections import Counter
from ..catalog import security_policy, live_or_static_catalog
from ..sql_guard import SQLGuard
from ..database import explain
from ..llm import structured_chat, compact_json
from ..models import CandidateChoice
from ..catalog import prompt


def validate_candidates(state):
    guard = SQLGuard(security_policy(), live_or_static_catalog())
    checked = []
    for cand in state.get("candidates", []):
        result = guard.validate(cand["sql"])
        item = dict(cand)
        item.update({
            "valid": result.ok,
            "normalized_sql": result.normalized_sql,
            "validation_error": result.error,
        })
        if result.ok and result.sql:
            try:
                explain(result.sql)
                item["sql"] = result.sql
                item["dry_run_error"] = None
            except Exception as exc:
                item["valid"] = False
                item["dry_run_error"] = str(exc)[:1200]
        checked.append(item)

    valid = [c for c in checked if c.get("valid") and c.get("normalized_sql")]
    selected = ""
    if len(valid) == 1:
        selected = valid[0]["sql"]
    elif len(valid) > 1:
        counts = Counter(c["normalized_sql"] for c in valid)
        winner, votes = counts.most_common(1)[0]
        if votes > 1:
            selected = next(c["sql"] for c in valid if c["normalized_sql"] == winner)
        else:
            # Self-consistency tie-break: all choices passed deterministic checks, so use
            # a narrow semantic judge rather than trusting generation order.
            choice = structured_chat(
                CandidateChoice,
                prompt("candidate_judge_system"),
                prompt(
                    "candidate_judge_user",
                    question=state["question"],
                    plan=compact_json(state.get("plan", {})),
                    schema=compact_json(state.get("schema_context", {})),
                    valid_candidates=compact_json([c["sql"] for c in valid]),
                ),
            )
            idx = max(0, min(choice.candidate_index, len(valid) - 1))
            selected = valid[idx]["sql"]

    errors = [c.get("validation_error") or c.get("dry_run_error") for c in checked if not c.get("valid")]
    return {
        "candidates": checked,
        "selected_sql": selected,
        "validation_error": " | ".join(e for e in errors if e)[:3000],
    }
