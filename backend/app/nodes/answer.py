from __future__ import annotations
from ..llm import text_chat, compact_json
from ..catalog import display_rules, prompt


def build_answer(state):
    rows = state.get("result_rows", [])
    user_prompt = prompt(
        "answer_user",
        question=state["question"],
        columns=state.get("result_columns", []),
        rows=compact_json(rows),
        display_rules=compact_json(display_rules(state.get("plan", {}).get("tables", []))),
        sql=state.get("selected_sql", ""),
    )
    answer = text_chat(prompt("answer_system"), user_prompt)
    return {"answer": answer}
