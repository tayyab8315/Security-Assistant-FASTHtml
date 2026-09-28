from __future__ import annotations
from ..database import execute_select


def execute_query(state):
    try:
        columns, rows = execute_select(state["selected_sql"])
        return {"result_columns": columns, "result_rows": rows, "status": "ok"}
    except Exception as exc:
        return {"status": "error", "error": f"Execution failed after successful dry-run: {str(exc)[:1500]}"}
