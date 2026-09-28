from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .config import ROOT, settings
from .database import inspect_live_schema


def load_json(name: str) -> Any:
    return json.loads((settings.domain_dir / name).read_text(encoding="utf-8"))


def load_admin_json(name: str) -> Any:
    return json.loads((ROOT / "admin" / name).read_text(encoding="utf-8"))


def security_policy() -> dict[str, Any]:
    return load_json("security_policy.json")


def static_catalog() -> dict[str, Any]:
    return load_admin_json("schema_catalog.json")


def business_glossary() -> dict[str, Any]:
    return load_json("business_glossary.json")


def display_rules(tables: list[str]) -> dict[str, Any]:
    """Return presentation rules only for planned, policy-approved tables."""
    rules = load_json("display_rules.json")
    policy = security_policy()
    allowed = set(policy["allowed_tables"]) - set(policy.get("blocked_tables", []))
    selected = {}
    for table in dict.fromkeys(tables):
        if table not in allowed or table not in rules.get("tables", {}):
            continue
        entry = dict(rules["tables"][table])
        blocked = set(policy.get("blocked_columns", {}).get(table, []))
        entry["columns"] = {name: rule for name, rule in entry.get("columns", {}).items()
                            if name not in blocked}
        selected[table] = entry
    return {"defaults": rules.get("defaults", {}), "tables": selected}


def examples() -> list[dict[str, Any]]:
    return load_admin_json("examples.json")


def prompt(name: str, **values: Any) -> str:
    """Load an LLM prompt template and substitute its named values."""
    templates = load_admin_json("prompts.json")
    try:
        template = templates[name]
    except KeyError as exc:
        raise KeyError(f"Prompt template not found: {name}") from exc
    return template.format(**values)


def project_relationships(catalog: dict[str, Any]) -> dict[str, Any]:
    """Expose semantic joins only when both endpoints survive policy/schema projection."""
    tables = catalog.get('tables', {})
    catalog['relationships'] = [
        rel for rel in catalog.get('relationships', [])
        if all(rel.get(column_key) in tables.get(rel.get(table_key), {}).get('columns', {})
               for table_key, column_key in [('from_table', 'from_column'), ('to_table', 'to_column')])
    ]
    return catalog


def live_or_static_catalog() -> dict[str, Any]:
    policy = security_policy()
    allowed = set(policy["allowed_tables"]) - set(policy.get("blocked_tables", []))
    blocked = {k: set(v) for k, v in policy.get("blocked_columns", {}).items()}
    base = static_catalog()

    # Apply the same security projection to the static fallback that is used for
    # live introspection. Sensitive columns must never enter embeddings/prompts.
    base["tables"] = {k: v for k, v in base.get("tables", {}).items() if k in allowed}
    for table, info in base["tables"].items():
        info["columns"] = {
            c: d for c, d in info.get("columns", {}).items()
            if c not in blocked.get(table, set())
        }

    try:
        live = inspect_live_schema(allowed, blocked)
    except Exception:
        # Useful before the DB is configured; exact live introspection is recommended for production.
        return project_relationships(base)

    # Once live introspection succeeds, only index tables that actually exist.
    live_tables = live.get("tables", {})
    base["tables"] = {k: v for k, v in base["tables"].items() if k in live_tables}
    for table, info in live_tables.items():
        base_table = base["tables"].setdefault(table, {"description": table, "columns": {}})
        description_map = base_table.get("columns", {})
        base_table["live_columns"] = info["columns"]
        base_table["foreign_keys"] = info["foreign_keys"]
        base_table["columns"] = {
            c["name"]: description_map.get(c["name"], f"Column {c['name']} ({c['type']}).")
            for c in info["columns"]
        }
    return project_relationships(base)
