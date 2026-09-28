from __future__ import annotations
from typing import Any, TypedDict

class Text2SQLState(TypedDict, total=False):
    question: str
    conversation_context: dict[str, Any]
    conversation_id: str
    intent: dict[str, Any]
    plan: dict[str, Any]
    schema_context: dict[str, Any]
    retrieved_tables: list[str]
    examples: list[dict[str, Any]]
    sampled_values: dict[str, list[Any]]
    resolved_entities: list[dict[str, Any]]
    entity_resolution_status: str
    entity_resolution_ambiguities: list[dict[str, Any]]
    candidates: list[dict[str, Any]]
    selected_sql: str
    repair_attempts: int
    validation_error: str
    result_columns: list[str]
    result_rows: list[dict[str, Any]]
    answer: str
    status: str
    clarification_question: str
    error: str
