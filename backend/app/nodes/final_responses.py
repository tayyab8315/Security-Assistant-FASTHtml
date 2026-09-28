from __future__ import annotations

from ..catalog import prompt
from ..llm import text_chat


def _reason(state) -> str:
    return state.get("intent", {}).get("short_reason") or "The request cannot be completed with the available capability."


def handle_knowledge_query(state):
    answer = text_chat(
        prompt("knowledge_answer_system"),
        prompt("knowledge_answer_user", question=state["question"], reason=_reason(state)),
    )
    return {"status": "knowledge_not_found", "answer": answer}


def handle_general_chat(state):
    answer = text_chat(
        prompt("general_chat_answer_system"),
        prompt("general_chat_answer_user", question=state["question"], reason=_reason(state)),
    )
    return {"answer": answer}


def handle_out_of_scope(state):
    answer = text_chat(
        prompt("out_of_scope_answer_system"),
        prompt("out_of_scope_answer_user", question=state["question"], reason=_reason(state)),
    )
    return {"answer": answer}


def handle_unsafe_request(state):
    answer = text_chat(
        prompt("unsafe_answer_system"),
        prompt("unsafe_answer_user", reason=_reason(state)),
    )
    return {"answer": answer}
