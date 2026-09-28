from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from ..config import settings
from ..nodes.answer import build_answer
from ..nodes.execute import execute_query
from ..nodes.generate import generate_candidates
from ..nodes.plan import make_plan
from ..nodes.repair import repair_sql
from ..nodes.retrieve import retrieve_context
from ..nodes.validate import validate_candidates
from ..state import Text2SQLState
from ..tracing import traced_step


def route_validation(state: Text2SQLState) -> str:
    if state.get("selected_sql"):
        return "execute"
    if state.get("repair_attempts", 0) < settings.max_repair_attempts:
        return "repair"
    return "failed"


def mark_failed(state: Text2SQLState) -> dict[str, str]:
    return {
        "status": "error",
        "error": "No safe SQL candidate passed deterministic validation and database EXPLAIN.",
    }


class DatabaseQueryService:
    """Reusable read-only database query workflow.

    The service begins after intent routing has classified a request as
    ``database_query``. It preserves the established plan → retrieve →
    generate → validate/repair → execute → answer sequence.
    """

    def __init__(self) -> None:
        self._graph = self._build_graph()

    @staticmethod
    def _build_graph():
        graph = StateGraph(Text2SQLState)
        nodes = [
            ("make_plan", make_plan, "Yes"),
            ("retrieve", retrieve_context, "No"),
            ("generate", generate_candidates, "Yes"),
            ("validate", validate_candidates, "Conditional (candidate judge)"),
            ("repair", repair_sql, "Yes"),
            ("execute", execute_query, "No"),
            ("build_answer", build_answer, "Yes"),
            ("failed", mark_failed, "No"),
        ]
        for name, node, llm in nodes:
            graph.add_node(name, traced_step(name.replace("_", " ").capitalize(), llm)(node))

        graph.add_edge(START, "retrieve")
        graph.add_edge("retrieve", "make_plan")
        graph.add_edge("make_plan", "generate")
        graph.add_edge("generate", "validate")
        graph.add_conditional_edges(
            "validate",
            route_validation,
            {"execute": "execute", "repair": "repair", "failed": "failed"},
        )
        graph.add_edge("repair", "validate")
        graph.add_conditional_edges(
            "execute",
            lambda state: "answer" if state.get("status") == "ok" else "end",
            {"answer": "build_answer", "end": END},
        )
        graph.add_edge("build_answer", END)
        graph.add_edge("failed", END)
        return graph.compile()

    def run(self, state: Text2SQLState) -> dict[str, Any]:
        return self._graph.invoke(state)


database_query_service = DatabaseQueryService()
