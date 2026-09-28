from __future__ import annotations
from ..llm import structured_chat, compact_json
from ..models import GeneratedSQL
from ..config import settings
from ..catalog import prompt


def repair_sql(state):
    attempts = state.get("repair_attempts", 0) + 1
    failed = state.get("candidates", [])
    selected_tables = state.get("retrieved_tables") or state.get("plan", {}).get("tables", [])
    all_query_rules = state.get("schema_context", {}).get("business_glossary", {}).get("query_rules", {})
    query_rules = {table: all_query_rules[table] for table in selected_tables if table in all_query_rules}
    user_prompt = prompt(
        "sql_repair_user",
        dialect=settings.sql_dialect,
        question=state["question"],
        plan=compact_json(state["plan"]),
        schema=compact_json(state["schema_context"]),
        query_rules=compact_json(query_rules),
        failed_candidates=compact_json(failed),
    )
    generated = structured_chat(GeneratedSQL, prompt("sql_repair_system"), user_prompt)
    return {"candidates": [{"sql": generated.sql, "valid": False}], "repair_attempts": attempts}
