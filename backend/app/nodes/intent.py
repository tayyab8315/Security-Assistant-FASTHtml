from __future__ import annotations

from ..catalog import live_or_static_catalog, prompt, security_policy
from ..llm import compact_json, structured_chat
from ..models import IntentUnderstanding
from ..config import settings
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def temporal_context():
    now = datetime.now(timezone.utc)
    name = settings.business_timezone.strip()
    if name:
        try:
            local = now.astimezone(ZoneInfo(name))
            return {"business_timezone": name, "current_datetime": local.isoformat(),
                    "current_date": local.date().isoformat(), "current_weekday": local.strftime("%A")}
        except ZoneInfoNotFoundError:
            pass
    return {"business_timezone": None, "current_utc_datetime": now.isoformat(),
            "note": "Business timezone unavailable; UTC is not an assumed business date."}



def reconcile_completeness(decision, allowed_tables):
    """Resolve contradictory flags only when the model supplies no blocker."""
    blockers = (
        decision.needs_clarification or decision.missing_required_context
        or any(item.strip() for item in decision.missing_information)
        or any(item.strip() for item in decision.ambiguity)
        or decision.clarification_items
        or (decision.clarification_question or "").strip()
    )
    if blockers:
        decision.needs_clarification = True
        decision.task_complete = False
    elif (not decision.task_complete and decision.intent == 'database_query'
          and decision.confidence >= 0.60
          and (decision.resolved_question or '').strip()
          and decision.required_tables
          and set(decision.required_tables).issubset(allowed_tables)):
        # task_complete means ready for downstream processing, not query executed.
        decision.task_complete = True
    return decision


def analyze_intent(state):
    catalog = live_or_static_catalog()
    policy = security_policy()
    allowed = set(policy["allowed_tables"]) - set(policy.get("blocked_tables", []))
    summary = {
        "tables": {
            table: {"description": info.get("description", "")}
            for table, info in catalog["tables"].items()
            if table in allowed
        }
    }
    decision = structured_chat(
        IntentUnderstanding,
        prompt("intent_system"),
        prompt("intent_user", question=state["question"], database_capability=compact_json(summary), conversation_context=compact_json(state.get("conversation_context", {})), temporal_context=compact_json(temporal_context())),
    )
    # Defer only explicitly classified value/column lookup questions to the
    # policy-filtered resolver. Other missing context must still stop execution.
    if (settings.enable_entity_resolution and decision.intent == "database_query"
            and decision.entity_values and decision.clarification_items):
        remaining = [item for item in decision.clarification_items if item.kind != "entity_reference"]
        decision.clarification_items = remaining
        decision.missing_information = [item.question for item in remaining]
        decision.clarification_question = " ".join(item.question for item in remaining) or None
        decision.needs_clarification = bool(remaining) or decision.missing_required_context
        decision.task_complete = not decision.needs_clarification
    resolved = (decision.resolved_question or "").strip()
    if not resolved and not state.get("conversation_context"):
        # A first-turn request is already the source of truth; preserve it when
        # optional model fields are omitted rather than storing an empty task.
        resolved = state["question"]
        decision.resolved_question = resolved
    if state.get("conversation_context") and not resolved and not decision.needs_clarification:
        decision.needs_clarification = True
        decision.task_complete = False
        decision.clarification_question = "Please restate the complete request, including the records or filters you mean."
    if decision.missing_required_context:
        decision.needs_clarification = True
        decision.task_complete = False
    decision = reconcile_completeness(decision, allowed)
    return {"intent": decision.model_dump(),
            "question": resolved or state["question"],
            "clarification_question": decision.clarification_question or ""}
