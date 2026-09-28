from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.scope import traverse_scope
from .config import MAX_RESULT_ROWS, settings


@dataclass
class GuardResult:
    ok: bool
    sql: str | None = None
    normalized_sql: str | None = None
    error: str | None = None


class SQLGuard:
    def __init__(self, policy: dict[str, Any], catalog: dict[str, Any]):
        self.allowed_tables = {t.lower() for t in policy["allowed_tables"]}
        self.blocked_tables = {t.lower() for t in policy.get("blocked_tables", [])}
        self.blocked_columns = {k.lower(): {c.lower() for c in v} for k, v in policy.get("blocked_columns", {}).items()}
        self.catalog = catalog

    def validate(self, sql: str) -> GuardResult:
        try:
            parsed = sqlglot.parse(sql, read=settings.sql_dialect)
        except Exception as exc:
            return GuardResult(False, error=f"SQL parse error: {exc}")
        if len(parsed) != 1:
            return GuardResult(False, error="Exactly one SQL statement is allowed.")
        tree = parsed[0]
        if not isinstance(tree, exp.Query):
            return GuardResult(False, error="Only read-only SELECT/query statements are allowed.")

        dangerous = (exp.Insert, exp.Update, exp.Delete, exp.Create, exp.Drop, exp.Alter, exp.Command, exp.Merge)
        if any(tree.find(t) is not None for t in dangerous):
            return GuardResult(False, error="DML/DDL/command statements are forbidden.")

        tables = {t.name.lower() for t in tree.find_all(exp.Table)}
        if any(t.db or t.catalog for t in tree.find_all(exp.Table)):
            return GuardResult(False, error="Cross-database table references are not allowed.")
        if not tables:
            return GuardResult(False, error="A query must read from at least one allowed business table.")
        forbidden = (tables - self.allowed_tables) | (tables & self.blocked_tables)
        if forbidden:
            return GuardResult(False, error=f"Forbidden or unknown table(s): {sorted(forbidden)}")

        # Block DB/server inspection and deliberate delay/file functions even inside SELECT.
        dangerous_functions = {
            "sleep", "benchmark", "load_file", "pg_read_file", "pg_read_binary_file",
            "pg_ls_dir", "pg_stat_file", "dblink", "lo_import", "lo_export"
        }
        for func in tree.find_all(exp.Func):
            if isinstance(func, exp.Anonymous):
                name = (func.name or "").lower()
            else:
                name = (getattr(func, "sql_name", lambda: "")() or "").lower()
            if name in dangerous_functions:
                return GuardResult(False, error=f"Forbidden SQL function: {name}")

        # Resolve aliases within each SELECT scope. A protected HR field must
        # remain protected as h.bank_account_number or inside a subquery, while
        # a table-specific block on notes must not block unrelated patrol notes.
        try:
            for scope in traverse_scope(tree):
                for col in scope.columns:
                    name = col.name.lower()
                    current = scope
                    sources = []
                    while current is not None:
                        if col.table:
                            sources = [source for alias, source in current.sources.items()
                                       if alias.lower() == col.table.lower()]
                            if sources:
                                break
                        else:
                            sources.extend(current.sources.values())
                        current = current.parent
                    for source in sources:
                        if isinstance(source, exp.Table) and name in self.blocked_columns.get(source.name.lower(), set()):
                            return GuardResult(False, error=f"Sensitive column blocked: {source.name}.{col.name}")
        except Exception:
            return GuardResult(False, error="Unable to safely resolve SQL column sources.")

        # Prevent projection stars (SELECT * / SELECT t.*), while still allowing COUNT(*).
        for select in tree.find_all(exp.Select):
            for projection in select.expressions:
                target = projection.this if isinstance(projection, exp.Alias) else projection
                if isinstance(target, exp.Star) or (isinstance(target, exp.Column) and isinstance(target.this, exp.Star)):
                    return GuardResult(False, error="SELECT * is not allowed; name explicit safe columns.")

        limited = self._enforce_limit(tree)
        normalized = limited.sql(dialect=settings.sql_dialect, pretty=False)
        return GuardResult(True, sql=normalized, normalized_sql=normalized)

    def _enforce_limit(self, tree: exp.Expression) -> exp.Expression:
        cloned = tree.copy()
        cap = min(MAX_RESULT_ROWS, settings.max_row_limit)
        default = min(settings.default_row_limit, cap)
        limit_node = cloned.args.get("limit")
        current = default
        if isinstance(limit_node, exp.Limit):
            expression = limit_node.expression
            if isinstance(expression, exp.Literal) and expression.is_int:
                current = int(expression.this)
        # Replace FETCH/PERCENT/WITH TIES and nonliteral limits with a plain cap.
        # Only cap the outer query so aggregates still consider all matching rows.
        cloned.set("limit", exp.Limit(expression=exp.Literal.number(
            min(current, cap) if current >= 0 else default)))
        return cloned
