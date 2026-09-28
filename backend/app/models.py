from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000, pattern=r"\S")
    conversation_id: str | None = Field(default=None, max_length=120)
    request_id: str | None = Field(default=None, min_length=1, max_length=80, pattern=r"[A-Za-z0-9_-]+")

class ClarificationItem(BaseModel):
    kind: Literal['entity_reference', 'required_context']
    question: str


class IntentUnderstanding(BaseModel):
    intent: Literal['database_query','knowledge_query','general_chat','out_of_scope','unsafe_request']
    entities: list[str] = []
    entity_values: list[str] = Field(default_factory=list)
    clarification_items: list[ClarificationItem] = Field(default_factory=list)
    operation: str = 'unknown'
    filters: list[str] = []
    required_tables: list[str] = []
    missing_information: list[str] = []
    ambiguity: list[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    needs_clarification: bool = False
    clarification_question: str | None = None
    resolved_question: str | None = None
    clarification_relation: Literal['continuation', 'new_request'] = 'continuation'
    known_details: list[str] = Field(default_factory=list)
    short_reason: str = ''
    missing_required_context: bool = False
    task_complete: bool = Field(default=True, description="Enough information to proceed with the task; does not mean the database query has executed. False must identify an unresolved requirement.")

class QueryPlan(BaseModel):
    objective: str
    retrieval_query: str
    tables: list[str]
    columns: list[str] = Field(default_factory=list, description="Output fields or aggregate expressions only: explicitly requested fields and the minimum context needed to understand the answer. Use qualified source columns and descriptive aliases for expressions. Do not include fields needed only for joins, filters, grouping or sorting.")
    supporting_columns: list[str] = Field(default_factory=list, description="Allowed source columns needed internally for joins, filters, grouping, sorting or calculations, but not requested as output. Do not project these into the final result. Blocked columns remain forbidden.")
    filters: list[str] = []
    group_by: list[str] = []
    order_by: list[str] = []
    sql_guidance: list[str] = []
    limit: int | None = None
    requires_join: bool = False
    join_reason: str | None = None
    resolved_entities: list[dict[str, Any]] = []

class GeneratedSQL(BaseModel):
    sql: str

class CandidateChoice(BaseModel):
    candidate_index: int
    short_reason: str = ''
    missing_required_context: bool = False
    task_complete: bool = True

class CandidateSQL(BaseModel):
    sql: str
    normalized_sql: str | None = None
    valid: bool = False
    validation_error: str | None = None
    dry_run_error: str | None = None

class AskResponse(BaseModel):
    status: Literal['ok','clarification_required','knowledge_not_found','out_of_scope','unsafe_request','error']
    conversation_id: str | None = None
    answer: str | None = None
    clarification_question: str | None = None
    sql: str | None = None
    columns: list[str] = []
    rows: list[dict[str, Any]] = []
    retrieved_tables: list[str] = []
    debug: dict[str, Any] | None = None
