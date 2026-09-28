import pytest
from backend.app.catalog import static_catalog, security_policy, live_or_static_catalog, examples, business_glossary
from backend.app.sql_guard import SQLGuard


def test_only_business_tables_allowed():
    policy = security_policy()
    assert {'customers', 'guards', 'sites', 'users', 'shifts', 'attendance', 'incidents', 'invoices', 'timesheets'}.issubset(policy['allowed_tables'])
    assert set(policy['allowed_tables']) == set(static_catalog()['tables'])
    assert not set(policy['allowed_tables']) & set(policy['blocked_tables'])
    assert {"conversations", "threads", "auth_sessions", "client_ai_conversations", "finance_integrations", "roles"}.issubset(set(policy["blocked_tables"]))


def test_password_is_blocked():
    assert "password" in security_policy()["blocked_columns"]["users"]


def test_obsolete_shift_columns_and_relationships_are_removed():
    for catalog in (static_catalog(), live_or_static_catalog()):
        assert 'guard_id' not in catalog['tables']['shifts']['columns']
        assert 'site_id' in catalog['tables']['shifts']['columns']
        assert any(r['from_table'] == 'shifts' and r['from_column'] == 'site_id'
                   and r['to_table'] == 'sites' and r['to_column'] == 'id'
                   for r in catalog['relationships'])
        for rel in catalog['relationships']:
            for table_key, column_key in [('from_table', 'from_column'), ('to_table', 'to_column')]:
                assert not (rel[table_key] == 'shifts' and rel[column_key] == 'guard_id')


def test_static_fallback_filters_all_protected_fields():
    catalog = live_or_static_catalog()
    policy = security_policy()
    for table, info in catalog['tables'].items():
        assert not set(info['columns']) & set(policy['blocked_columns'].get(table, []))
    assert 'bank_account_number' not in catalog['tables']['hr_employee_profiles']['columns']
    assert 'notes' in catalog['tables']['patrol_logs']['columns']
    assert catalog['relationships']
    for rel in catalog['relationships']:
        assert rel['from_table'] in catalog['tables']
        assert rel['to_table'] in catalog['tables']


@pytest.mark.parametrize('example', examples(), ids=lambda ex: ex['question'])
def test_examples_reference_real_safe_columns(example):
    from sqlglot import parse_one, exp
    catalog = live_or_static_catalog()
    assert SQLGuard(security_policy(), catalog).validate(example['sql']).ok
    tree = parse_one(example['sql'], read='mysql')
    tables = {table.name for table in tree.find_all(exp.Table)}
    assert tables == set(example['tables'])
    table_aliases = {table.alias_or_name: table.name for table in tree.find_all(exp.Table)}
    aliases = {alias.alias for alias in tree.find_all(exp.Alias)}
    for column in tree.find_all(exp.Column):
        if column.table:
            assert column.name in catalog['tables'][table_aliases[column.table]]['columns']
        else:
            assert column.name in aliases or any(column.name in catalog['tables'][t]['columns'] for t in tables)
    edges = {frozenset(((r['from_table'], r['from_column']), (r['to_table'], r['to_column'])))
             for r in catalog['relationships']}
    for join in tree.find_all(exp.Join):
        for equality in join.args['on'].find_all(exp.EQ):
            left, right = equality.left, equality.right
            assert frozenset(((table_aliases[left.table], left.name), (table_aliases[right.table], right.name))) in edges


def test_sample_columns_are_safe_and_present():
    catalog = live_or_static_catalog()
    for table, columns in security_policy()['sample_value_columns'].items():
        assert set(columns).issubset(catalog['tables'][table]['columns'])


def test_role_rules_and_availability_source_are_documented():
    assert 'Numeric' in static_catalog()['tables']['users']['columns']['role_type']
    assert 'INT' in business_glossary()['query_rules']['users']['role_type'][0]
    glossary = business_glossary()
    assert not any(a['term'] == 'guard availability' for a in glossary['ambiguities'])
    assert any('guard availability' in s['terms'] and s['maps_to'] == 'guard_availabilities'
               for s in glossary['synonyms'])


def test_live_catalog_does_not_claim_missing_tables(monkeypatch):
    from backend.app import catalog
    monkeypatch.setattr(catalog, 'inspect_live_schema', lambda *args: {
        'tables': {'shifts': {'columns': [{'name': 'id', 'type': 'INT'}], 'foreign_keys': []}}
    })
    result = catalog.live_or_static_catalog()
    assert set(result['tables']) == {'shifts'}
    assert set(result['tables']['shifts']['columns']) == {'id'}
    assert result['relationships'] == []
