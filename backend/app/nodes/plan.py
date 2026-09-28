from __future__ import annotations
from ..llm import structured_chat, compact_json
from ..models import QueryPlan
from ..catalog import prompt

def make_plan(state):
    context = state.get("schema_context", {})
    tables = context.get("tables", {})
    if not tables:
        raise ValueError("No relevant table schemas were retrieved for query planning.")
    plan_context = {
        "tables": tables,
        "relationships": context.get("verified_relationships", [])
    }
    plan = structured_chat(
        QueryPlan,
        prompt("query_plan_system"),
        prompt(
            "query_plan_user",
            question=state["question"],
            intent=compact_json(state.get("intent",{})),
            catalog=compact_json(plan_context),
            glossary=compact_json(context.get("business_glossary", {})),
            resolved_entities=compact_json(state.get("resolved_entities", [])),
        ),
    )
    missing = set(plan.tables) - set(tables)
    if missing:
        raise ValueError(f"Planner requested tables outside the retrieved schema: {sorted(missing)}")
    plan = plan.model_copy(update={"resolved_entities": state.get("resolved_entities", [])})
    return {"plan": plan.model_dump()}
