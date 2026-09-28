from __future__ import annotations

import re
from collections import deque
from difflib import SequenceMatcher
from typing import Any

from .catalog import business_glossary, live_or_static_catalog, security_policy
from .database import search_value_candidates
from .config import settings


# Columns are classified from schema metadata, not hard-coded table names.  The
# classifier is intentionally conservative: it decides which values are useful
# for entity resolution, while the security policy remains the source of truth.
_NAME_HINTS = {
    "name", "first_name", "last_name", "full_name", "display_name", "username",
    "customer", "client", "site", "guard", "employee", "person", "supplier",
    "subcontractor", "email", "phone", "title", "code", "number", "city",
    "country", "department", "location", "category", "type", "status",
}
_ID_HINTS = {"id", "_id", "code", "number", "no", "key"}
_DATE_HINTS = {"date", "at", "time", "dob", "expiry", "created", "updated", "start", "end"}


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", _norm(value)))


def _column_semantic(table: str, column: str, description: str, db_type: str) -> str:
    text = f"{table} {column} {description}".lower()
    c = column.lower()
    t = db_type.lower()
    if "email" in text:
        return "email"
    if "phone" in text or "mobile" in text or "telephone" in text:
        return "phone"
    if any(x in c for x in ("dob", "birth", "date", "expiry", "created_at", "updated_at", "_at")) or "date" in t:
        return "date"
    if any(x in c for x in ("first_name", "last_name", "full_name", "display_name")):
        return "person_name"
    if c in {"customer", "client_name", "customer_name"}:
        return "customer_name"
    if c in {"site", "site_name", "location_name"}:
        return "site_name"
    if any(x in c for x in ("status", "state")):
        return "status"
    if any(x in c for x in ("category", "type", "kind")):
        return "category"
    if any(x in c for x in ("_id", "id", "code", "number", "no")):
        return "identifier"
    if any(x in text for x in ("name", "customer", "client", "site", "guard", "employee", "supplier", "title")):
        return "entity_name"
    if any(x in t for x in ("char", "text", "enum", "set")):
        return "text"
    if any(x in t for x in ("int", "decimal", "numeric", "float", "double")):
        return "numeric"
    return "other"


def _searchable_columns(catalog: dict[str, Any], policy: dict[str, Any]) -> list[dict[str, Any]]:
    blocked = {k: set(v) for k, v in policy.get("blocked_columns", {}).items()}
    allowed = set(policy.get("allowed_tables", [])) - set(policy.get("blocked_tables", []))
    rows: list[dict[str, Any]] = []
    for table, info in catalog.get("tables", {}).items():
        if table not in allowed:
            continue
        live_types = {c["name"]: str(c.get("type", "")) for c in info.get("live_columns", [])}
        for column, description in info.get("columns", {}).items():
            if column in blocked.get(table, set()):
                continue
            db_type = live_types.get(column, "")
            semantic = _column_semantic(table, column, str(description), db_type)
            # Free-form descriptions are deliberately excluded by default.
            if semantic in {"other", "date", "numeric"}:
                continue
            rows.append({
                "table": table,
                "column": column,
                "description": str(description),
                "db_type": db_type,
                "semantic_type": semantic,
            })
    return rows


def _filter_value_candidates(intent: dict[str, Any]) -> list[str]:
    """Extract literal values embedded in structured filter tokens.

    The intent model may return semantic entities such as ``guard`` and ``site``.
    Those are schema concepts, not database values.  Filter tokens are a much
    safer source for literals such as ``guard_name_contains_ali``.
    """
    values: list[str] = []
    for item in intent.get("filters", []) or []:
        if not isinstance(item, str):
            continue
        text = item.strip()
        if not text:
            continue
        # Common structured form: <field>_<operator>_<value>
        m = re.search(r"(?:^|_)(?:contains|equals|equal|is|starts_with|ends_with|like)_([^_]+(?:_[^_]+)*)$", text, flags=re.I)
        if m:
            raw = m.group(1).replace("_", " ").strip()
            if raw:
                values.append(raw)
            continue
        # Common form: <field>_contains_<value> where the value may be one word.
        m = re.search(r"_contains_([^\s]+(?:\s+[^\s]+)*)$", text, flags=re.I)
        if m:
            values.append(m.group(1).strip())
    return values


def _is_schema_concept(text: str, catalog: dict[str, Any]) -> bool:
    """Return True when text is a schema/entity concept rather than a value."""
    key = _norm(text)
    if not key:
        return True
    table_names = {_norm(t) for t in catalog.get("tables", {}).keys()}
    if key in table_names:
        return True
    # Generic domain nouns should never be sent to the live value resolver just
    # because the intent LLM placed them in ``entities``.
    generic = {
        "guard", "guards", "site", "sites", "customer", "customers",
        "client", "clients", "user", "users", "employee", "employees",
        "incident", "incidents", "shift", "shifts", "attendance",
        "supplier", "suppliers", "visitor", "visitors", "contract",
        "contracts", "invoice", "invoices", "patrol", "patrols",
        "leave", "leaves", "request", "requests", "role", "roles",
        "security", "status", "record", "records", "data", "information",
    }
    return key in generic


def _extract_entity_texts(question: str, intent: dict[str, Any], catalog: dict[str, Any]) -> list[str]:
    values: list[str] = [v for v in intent.get("entity_values", []) if isinstance(v, str) and v.strip()]

    # 1) Structured filters are the preferred source of literal values.
    values.extend(_filter_value_candidates(intent))

    # 2) Quoted literals are unambiguously values.
    for match in re.findall(r"[\"']([^\"']{2,100})[\"']", question):
        values.append(match.strip())

    # 3) Natural-language value phrases.  Capture only the value immediately
    # following a relation/name cue, not nouns such as "guard" or "site".
    patterns = [
        r"\b(?:assigned\s+to|reported\s+by|managed\s+by|owned\s+by|created\s+by|approved\s+by|requested\s+by|for|by|from|at|named|called)\s+(?:the\s+)?(?:guard|site|customer|client|user|employee|supplier|person|employee\s+code)?\s*(?:named\s+|called\s+)?([A-Za-z][A-Za-z0-9 ._-]{1,80})",
        r"\b(?:guard|site|customer|client|user|employee|supplier|person)\s+(?:named|called)\s+([A-Za-z][A-Za-z0-9 ._-]{1,80})",
    ]
    stop_words = r"\b(?:with|having|who|that|where|and|on|in|during|from|for|assigned|reported|show|all|the)\b"
    for pattern in patterns:
        for match in re.findall(pattern, question, flags=re.I):
            value = re.split(stop_words, match, maxsplit=1, flags=re.I)[0].strip(" ,.?;:")
            if 2 <= len(value) <= 80 and not _is_schema_concept(value, catalog):
                values.append(value)

    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = _norm(value)
        if key and not _is_schema_concept(value, catalog) and key not in seen:
            seen.add(key)
            out.append(value)
    return out


def _relationship_distance(catalog: dict[str, Any], source: str, targets: set[str]) -> int | None:
    if not targets:
        return None
    if source in targets:
        return 0
    graph: dict[str, set[str]] = {}
    for rel in catalog.get("relationships", []):
        a, b = rel.get("from_table"), rel.get("to_table")
        if not a or not b:
            continue
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    q: deque[tuple[str, int]] = deque([(source, 0)])
    seen = {source}
    while q:
        node, dist = q.popleft()
        for nxt in graph.get(node, set()):
            if nxt in seen:
                continue
            if nxt in targets:
                return dist + 1
            seen.add(nxt)
            q.append((nxt, dist + 1))
    return None


def _candidate_score(candidate: dict[str, Any], entity: str, targets: set[str], glossary: dict[str, Any]) -> float:
    score = {"exact": 1.00, "prefix": 0.88, "contains": 0.74}.get(candidate.get("match_type"), 0.50)
    semantic = candidate.get("semantic_type", "")
    value_tokens = _tokens(entity)
    column_tokens = _tokens(candidate.get("column", ""))
    if value_tokens & column_tokens:
        score += 0.04
    distance = _relationship_distance(glossary.get("_catalog", {}), candidate["table"], targets)
    if distance == 0:
        score += 0.22
    elif distance is not None:
        score += max(0.0, 0.14 - 0.025 * distance)
    return score


def resolve_entities(state: dict[str, Any]) -> dict[str, Any]:
    intent = state.get("intent", {})
    if not settings.enable_entity_resolution or intent.get("intent") != "database_query":
        return {"resolved_entities": [], "entity_resolution_status": "not_applicable"}

    catalog = live_or_static_catalog()
    policy = security_policy()
    glossary = business_glossary()
    glossary = dict(glossary)
    glossary["_catalog"] = catalog
    entity_texts = _extract_entity_texts(state.get("question", ""), intent, catalog)
    if not entity_texts:
        return {"resolved_entities": [], "entity_resolution_status": "none"}

    columns = _searchable_columns(catalog, policy)[: max(1, settings.entity_resolution_columns_limit)]
    targets = {t for t in intent.get("required_tables", []) if t in catalog.get("tables", {})}
    resolved: list[dict[str, Any]] = []
    ambiguities: list[dict[str, Any]] = []

    for entity in entity_texts:
        raw_candidates = search_value_candidates(entity, columns, limit_per_column=settings.entity_resolution_matches_per_column)
        candidates: list[dict[str, Any]] = []
        for c in raw_candidates:
            item = dict(c)
            item["score"] = round(_candidate_score(item, entity, targets, glossary), 4)
            candidates.append(item)
        candidates.sort(key=lambda x: (-x["score"], x["table"], x["column"], str(x.get("matched_value", ""))))
        if not candidates:
            continue

        # Multiple name columns on the SAME entity table are normally one
        # semantic predicate.  For example, "Ali" matching guards.first_name
        # and guards.last_name should become:
        #   guards.first_name = 'Ali' OR guards.last_name = 'Ali'
        # rather than an unnecessary clarification.
        top = candidates[0]
        near = [c for c in candidates if c["score"] >= top["score"] - 0.08]
        near_tables = {c["table"] for c in near}
        same_person_name_group = (
            len(near_tables) == 1
            and top.get("semantic_type") in {"person_name", "entity_name", "customer_name", "site_name"}
            and all(c.get("semantic_type") in {"person_name", "entity_name", "customer_name", "site_name"} for c in near)
        )
        if same_person_name_group:
            resolved.append({
                "text": entity,
                "normalized_value": _norm(entity),
                "resolved_table": top["table"],
                "resolved_column": top["column"],
                "resolved_columns": sorted({c["column"] for c in near}),
                "predicate_strategy": "same_table_any_name_column",
                "matched_value": top.get("matched_value"),
                "match_type": top.get("match_type"),
                "confidence": min(0.99, max(0.0, top["score"] / 1.25)),
                "candidates": candidates[:8],
            })
            continue

        # Different entity tables remain ambiguous unless relationship context
        # gives a sufficiently strong separation.
        if len(near_tables) > 1:
            ambiguities.append({
                "text": entity,
                "candidates": near[:8],
            })
            continue

        resolved.append({
            "text": entity,
            "normalized_value": _norm(entity),
            "resolved_table": top["table"],
            "resolved_column": top["column"],
            "matched_value": top.get("matched_value"),
            "match_type": top.get("match_type"),
            "confidence": min(0.99, max(0.0, top["score"] / 1.25)),
            "candidates": candidates[:5],
        })

    if ambiguities:
        parts = []
        for a in ambiguities:
            options = ", ".join(f"{c['table']}.{c['column']}={c.get('matched_value')}" for c in a["candidates"][:4])
            parts.append(f"'{a['text']}' matched multiple data entities ({options}).")
        question = "Please clarify which record you mean. " + " ".join(parts)
        return {
            "resolved_entities": resolved,
            "entity_resolution_status": "ambiguous",
            "entity_resolution_ambiguities": ambiguities,
            "clarification_question": question,
        }

    return {
        "resolved_entities": resolved,
        "entity_resolution_status": "resolved" if resolved else "unresolved",
    }
