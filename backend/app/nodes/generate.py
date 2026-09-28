from __future__ import annotations
from ..llm import structured_chat, compact_json
from ..models import GeneratedSQL
from ..config import settings
from ..catalog import prompt


def generate_candidates(state):
    selected_tables = state.get("retrieved_tables") or state.get("plan", {}).get("tables", [])
    all_query_rules = state.get("schema_context", {}).get("business_glossary", {}).get("query_rules", {})
    query_rules = {table: all_query_rules[table] for table in selected_tables if table in all_query_rules}
    user_prompt = prompt(
        "sql_generate_user",
        dialect=settings.sql_dialect,
        question=state["question"],
        plan=compact_json(state["plan"]),
        schema_context=compact_json(state["schema_context"]),
        sampled_values=compact_json(state.get("sampled_values", {})),
        query_rules=compact_json(query_rules),
        examples=compact_json(state.get("examples", [])),
    )
    candidates = []
    for i in range(max(1, settings.sql_candidates)):
        generated = structured_chat(GeneratedSQL, prompt("sql_generate_system"), user_prompt + prompt("sql_candidate_variant", variant=i + 1), temperature=min(0.15 * i, 0.3))
        candidates.append({"sql": generated.sql, "valid": False})
    return {"candidates": candidates, "repair_attempts": state.get("repair_attempts", 0)}
