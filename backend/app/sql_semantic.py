from dataclasses import dataclass
@dataclass
class SemanticResult:
    ok: bool
    reason: str = ""
def validate_semantics(question: str, sql: str) -> SemanticResult:
    q=question.lower()
    s=sql.lower()
    if ("how many" in q or "count" in q) and "count(" not in s:
        return SemanticResult(False,"Expected aggregation")
    return SemanticResult(True)
