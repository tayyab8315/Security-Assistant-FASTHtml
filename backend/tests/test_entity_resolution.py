from unittest.mock import patch

from backend.app.entity_resolver import _column_semantic, resolve_entities


def test_column_semantics_are_generic():
    assert _column_semantic("guards", "first_name", "Guard first name", "VARCHAR(80)") == "person_name"
    assert _column_semantic("sites", "site", "Site display/name", "VARCHAR(120)") == "site_name"
    assert _column_semantic("customers", "customer", "Customer display/name", "VARCHAR(120)") == "customer_name"
    assert _column_semantic("incidents", "status", "Recorded status", "ENUM") == "status"


def test_resolver_uses_relationship_context_to_disambiguate(monkeypatch):
    catalog = {
        "tables": {
            "guards": {"columns": {"first_name": "Guard first name"}},
            "users": {"columns": {"name": "System user name"}},
            "sites": {"columns": {"site": "Site name"}},
        },
        "relationships": [
            {"from_table": "users", "from_column": "guard_id", "to_table": "guards", "to_column": "id"},
            {"from_table": "shifts", "from_column": "site_id", "to_table": "sites", "to_column": "id"},
            {"from_table": "shift_assignments", "from_column": "guard_id", "to_table": "guards", "to_column": "id"},
            {"from_table": "shift_assignments", "from_column": "shift_id", "to_table": "shifts", "to_column": "id"},
        ],
    }
    policy = {"allowed_tables": ["guards", "users", "sites"], "blocked_tables": [], "blocked_columns": {}}
    monkeypatch.setattr("backend.app.entity_resolver.live_or_static_catalog", lambda: catalog)
    monkeypatch.setattr("backend.app.entity_resolver.security_policy", lambda: policy)
    monkeypatch.setattr("backend.app.entity_resolver.business_glossary", lambda: {})
    monkeypatch.setattr("backend.app.entity_resolver.search_value_candidates", lambda value, columns, limit_per_column=4: [
        {"table": "guards", "column": "first_name", "matched_value": "Ali", "match_type": "exact", "semantic_type": "person_name"},
        {"table": "users", "column": "name", "matched_value": "Ali", "match_type": "exact", "semantic_type": "entity_name"},
    ])
    result = resolve_entities({
        "question": "show sites assigned to Ali",
        "intent": {"intent": "database_query", "entities": ["Ali"], "required_tables": ["guards", "sites", "shift_assignments", "shifts"]},
    })
    assert result["entity_resolution_status"] == "resolved"
    assert result["resolved_entities"][0]["resolved_table"] == "guards"
    assert result["resolved_entities"][0]["resolved_column"] == "first_name"


def test_resolver_returns_ambiguity_when_two_candidates_are_equally_relevant(monkeypatch):
    catalog = {
        "tables": {
            "guards": {"columns": {"first_name": "Guard first name"}},
            "users": {"columns": {"name": "System user name"}},
        },
        "relationships": [],
    }
    policy = {"allowed_tables": ["guards", "users"], "blocked_tables": [], "blocked_columns": {}}
    monkeypatch.setattr("backend.app.entity_resolver.live_or_static_catalog", lambda: catalog)
    monkeypatch.setattr("backend.app.entity_resolver.security_policy", lambda: policy)
    monkeypatch.setattr("backend.app.entity_resolver.business_glossary", lambda: {})
    monkeypatch.setattr("backend.app.entity_resolver.search_value_candidates", lambda value, columns, limit_per_column=4: [
        {"table": "guards", "column": "first_name", "matched_value": "Ali", "match_type": "exact", "semantic_type": "person_name"},
        {"table": "users", "column": "name", "matched_value": "Ali", "match_type": "exact", "semantic_type": "entity_name"},
    ])
    result = resolve_entities({
        "question": "show details for Ali",
        "intent": {"intent": "database_query", "entities": ["Ali"], "required_tables": []},
    })
    assert result["entity_resolution_status"] == "ambiguous"
    assert result["entity_resolution_ambiguities"]


def test_blocked_columns_are_not_present_in_searchable_projection(monkeypatch):
    from backend.app.entity_resolver import _searchable_columns
    catalog = {"tables": {"users": {"columns": {"name": "Name", "password": "Password"}}}}
    policy = {"allowed_tables": ["users"], "blocked_tables": [], "blocked_columns": {"users": ["password"]}}
    cols = _searchable_columns(catalog, policy)
    assert {(c["table"], c["column"]) for c in cols} == {("users", "name")}


def test_resolver_ignores_schema_concepts_and_extracts_filter_value(monkeypatch):
    catalog = {
        "tables": {
            "guards": {"columns": {
                "first_name": "Guard first name",
                "last_name": "Guard last name",
            }},
            "sites": {"columns": {"site": "Site name"}},
        },
        "relationships": [],
    }
    policy = {"allowed_tables": ["guards", "sites"], "blocked_tables": [], "blocked_columns": {}}
    monkeypatch.setattr("backend.app.entity_resolver.live_or_static_catalog", lambda: catalog)
    monkeypatch.setattr("backend.app.entity_resolver.security_policy", lambda: policy)
    monkeypatch.setattr("backend.app.entity_resolver.business_glossary", lambda: {})
    monkeypatch.setattr("backend.app.entity_resolver.search_value_candidates", lambda value, columns, limit_per_column=4: [
        {"table": "guards", "column": "first_name", "matched_value": "Ali", "match_type": "exact", "semantic_type": "person_name"},
        {"table": "guards", "column": "last_name", "matched_value": "Ali", "match_type": "exact", "semantic_type": "person_name"},
    ] if value.lower() == "ali" else [])

    result = resolve_entities({
        "question": "show me all sites assigned to ali",
        "intent": {
            "intent": "database_query",
            "entities": ["guard", "site"],
            "filters": ["guard_name_contains_ali"],
            "required_tables": ["guards", "sites"],
        },
    })

    assert result["entity_resolution_status"] == "resolved"
    assert len(result["resolved_entities"]) == 1
    entity = result["resolved_entities"][0]
    assert entity["text"].lower() == "ali"
    assert entity["resolved_table"] == "guards"
    assert entity["predicate_strategy"] == "same_table_any_name_column"
    assert set(entity["resolved_columns"]) == {"first_name", "last_name"}
