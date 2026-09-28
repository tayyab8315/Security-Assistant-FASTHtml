from __future__ import annotations
from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine import make_url

from .config import MAX_RESULT_ROWS, settings

_engine: Engine | None = None


def engine() -> Engine:
    global _engine
    if _engine is None:
        url = settings.database_connection_url
        driver = make_url(url).drivername
        connect_args = {}
        if driver == "mysql+pymysql":
            connect_args = {
                "connect_timeout": settings.db_timeout_seconds,
                "read_timeout": settings.db_timeout_seconds,
                "write_timeout": settings.db_timeout_seconds,
            }
        elif driver.startswith("postgresql"):
            connect_args = {"connect_timeout": settings.db_timeout_seconds}
        _engine = create_engine(url, pool_pre_ping=True, future=True, connect_args=connect_args)
    return _engine


def inspect_live_schema(allowed_tables: set[str], blocked_columns: dict[str, set[str]]) -> dict[str, Any]:
    inspector = inspect(engine())
    available = set(inspector.get_table_names())
    tables: dict[str, Any] = {}
    for table in sorted(allowed_tables & available):
        columns = []
        for c in inspector.get_columns(table):
            if c["name"] in blocked_columns.get(table, set()):
                continue
            columns.append({"name": c["name"], "type": str(c.get("type", "")), "nullable": bool(c.get("nullable", True)), "default": str(c.get("default")) if c.get("default") is not None else None})
        fks = []
        for fk in inspector.get_foreign_keys(table):
            if (fk.get("referred_table") in allowed_tables
                    and not set(fk.get('constrained_columns', [])) & blocked_columns.get(table, set())
                    and not set(fk.get('referred_columns', [])) & blocked_columns.get(fk.get('referred_table'), set())):
                fks.append({"constrained_columns": fk.get("constrained_columns", []), "referred_table": fk.get("referred_table"), "referred_columns": fk.get("referred_columns", [])})
        tables[table] = {"columns": columns, "foreign_keys": fks}
    return {"tables": tables}


def explain(sql: str) -> None:
    with engine().connect() as conn:
        conn.execute(text("EXPLAIN " + sql))


def execute_select(sql: str) -> tuple[list[str], list[dict[str, Any]]]:
    with engine().connect() as conn:
        result = conn.execute(text(sql))
        return list(result.keys()), [dict(r._mapping) for r in result.fetchmany(min(MAX_RESULT_ROWS, settings.max_row_limit))]


def search_value_candidates(value: str, columns: list[dict[str, Any]], limit_per_column: int = 4) -> list[dict[str, Any]]:
    """Resolve a user value against all policy-approved searchable columns.

    Identifiers come exclusively from the trusted catalog; values are always
    bound parameters. Exact matching is attempted first, followed by prefix and
    contains matching only when exact matching returns no candidates.
    """
    import re

    if not value or not columns:
        return []

    def quote_identifier(identifier: str) -> str:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identifier):
            raise ValueError(f"Unsafe catalog identifier: {identifier}")
        return f"`{identifier}`"

    def run(mode: str) -> list[dict[str, Any]]:
        selects = []
        params: dict[str, Any] = {}
        for i, meta in enumerate(columns):
            table = quote_identifier(meta["table"])
            column = quote_identifier(meta["column"])
            param = f"v{i}"
            if mode == "exact":
                predicate = f"LOWER(CAST({column} AS CHAR)) = LOWER(:{param})"
                params[param] = value
            elif mode == "prefix":
                predicate = f"LOWER(CAST({column} AS CHAR)) LIKE LOWER(:{param})"
                params[param] = f"{value}%"
            else:
                predicate = f"LOWER(CAST({column} AS CHAR)) LIKE LOWER(:{param})"
                params[param] = f"%{value}%"
            selects.append(
                f"(SELECT '{meta['table']}' AS table_name, '{meta['column']}' AS column_name, "
                f"CAST({column} AS CHAR) AS matched_value, '{mode}' AS match_type "
                f"FROM {table} WHERE {predicate} LIMIT {int(limit_per_column)})"
            )
        sql = " UNION ALL ".join(selects)
        with engine().connect() as conn:
            rows = conn.execute(text(sql), params).mappings().fetchall()
        return [dict(row) for row in rows]

    exact = run("exact")
    if exact:
        by_key = {(r["table_name"], r["column_name"], str(r["matched_value"])): r for r in exact}
        results = list(by_key.values())
    else:
        results = run("prefix")
        if not results:
            results = run("contains")

    # Attach semantic metadata from the catalog to avoid another lookup.
    lookup = {(c["table"], c["column"]): c for c in columns}
    output = []
    for row in results:
        table_name = row.pop("table_name")
        column_name = row.pop("column_name")
        meta = lookup.get((table_name, column_name), {})
        output.append({
            **row,
            "table": table_name,
            "column": column_name,
            "semantic_type": meta.get("semantic_type", "text"),
            "description": meta.get("description", ""),
        })
    return output


def sample_distinct(table: str, column: str, limit: int = 8) -> list[Any]:
    query = text(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL LIMIT :limit")
    with engine().connect() as conn:
        return [r[0] for r in conn.execute(query, {"limit": limit}).fetchall()]
