from unittest.mock import Mock

from backend.app import vector_store


def test_column_ranking_does_not_hide_fields_or_restore_blocked_columns(monkeypatch):
    monkeypatch.setattr(vector_store, "embed_texts", lambda texts: [[0.1]])
    store = vector_store.SchemaVectorStore.__new__(vector_store.SchemaVectorStore)
    store.tables = Mock()
    store.tables.count.return_value = 2
    store.tables.query.return_value = {"metadatas": [[{"table": "guards"}, {"table": "stale_table"}]]}
    store.columns = Mock()
    store.columns.count.return_value = 2
    # Reproduce a ranking that omits gender and includes stale sensitive metadata.
    store.columns.query.return_value = {"metadatas": [[
        {"table": "guards", "column": "license_expiry"},
        {"table": "guards", "column": "guard_passport"},
    ]]}
    store.examples = Mock()
    store.examples.count.return_value = 0
    allowed_columns = {
        "first_name": "First name", "last_name": "Last name", "gender": "Gender",
        "dob": "Birth date", "license_expiry": "License expiry", "status": "1 active; 0 inactive",
    }
    result = store.retrieve("List active guards with gender and expiry dates", {
        "tables": {"guards": {"columns": allowed_columns}}
    })
    columns = result["schema_context"]["tables"]["guards"]["columns"]
    assert columns == allowed_columns
    assert list(columns)[0] == "license_expiry"
    assert result["tables"] == ["guards"]


def test_removed_index_examples_cannot_reintroduce_obsolete_columns(monkeypatch):
    monkeypatch.setattr(vector_store, 'embed_texts', lambda texts: [[0.1]])
    store = vector_store.SchemaVectorStore.__new__(vector_store.SchemaVectorStore)
    store.tables = Mock()
    store.tables.count.return_value = 1
    store.tables.query.return_value = {'metadatas': [[{'table': 'shifts'}]]}
    store.columns = Mock()
    store.columns.count.return_value = 1
    store.columns.query.return_value = {'metadatas': [[{'table': 'shifts', 'column': 'site_id'}]]}
    store.examples = Mock()
    store.examples.count.return_value = 1
    store.examples.query.return_value = {'metadatas': [[{
        'question': 'Old shift query', 'sql': 'SELECT guard_id, site_id FROM shifts', 'tables': 'shifts'
    }]]}
    result = store.retrieve('Show shifts', {'tables': {'shifts': {'columns': {'id': 'ID'}}}})
    assert result['examples'] == []
    assert result['schema_context']['tables']['shifts']['columns'] == {'id': 'ID'}
