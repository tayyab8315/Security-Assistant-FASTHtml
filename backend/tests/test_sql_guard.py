from backend.app.sql_guard import SQLGuard
from backend.app.catalog import security_policy, static_catalog
import pytest


def guard():
    return SQLGuard(security_policy(), static_catalog())


def test_allows_safe_select():
    r = guard().validate("SELECT id, first_name, last_name FROM guards LIMIT 20")
    assert r.ok


def test_blocks_conversation_table():
    r = guard().validate("SELECT conversation_id, content FROM conversations LIMIT 10")
    assert not r.ok


def test_blocks_password():
    r = guard().validate("SELECT user_id, password FROM users LIMIT 10")
    assert not r.ok


def test_blocks_select_star():
    r = guard().validate("SELECT * FROM users")
    assert not r.ok


def test_blocks_dml():
    r = guard().validate("DELETE FROM guards WHERE id = 1")
    assert not r.ok


def test_adds_limit():
    r = guard().validate("SELECT id, site FROM sites ORDER BY id")
    assert r.ok
    assert "LIMIT" in r.sql.upper()


def test_count_star_is_allowed():
    r = guard().validate("SELECT COUNT(*) AS guard_count FROM guards")
    assert r.ok


def test_no_table_query_is_blocked():
    r = guard().validate("SELECT CURRENT_USER")
    assert not r.ok


@pytest.mark.parametrize('sql', [
    'SELECT h.bank_account_number FROM hr_employee_profiles h',
    'SELECT U.PASSWORD FROM users U',
    'SELECT g.sia_license_number FROM guard_compliance g',
    'SELECT c.notes FROM guard_compliance c',
    'SELECT d.file_url FROM guard_documents d',
    'SELECT l.id FROM leave_requests l WHERE l.reason IS NOT NULL',
    'SELECT x.secret FROM (SELECT h.bank_account_number AS secret FROM hr_employee_profiles h) x',
    'SELECT h.id FROM hr_employee_profiles h WHERE EXISTS (SELECT s.id FROM shifts s WHERE h.bank_account_number IS NOT NULL)',
    'SELECT config_json FROM finance_integrations',
    'SELECT permissions FROM roles',
    'SELECT user_query FROM client_ai_conversations',
    'SELECT id FROM other_database.shifts',
])
def test_expanded_policy_blocks_sensitive_aliases_and_internal_tables(sql):
    assert not guard().validate(sql).ok


@pytest.mark.parametrize('sql', [
    'SELECT p.notes FROM patrol_logs p',
    'SELECT notes FROM patrol_logs',
    'SELECT h.guard_id, h.employment_type FROM hr_employee_profiles h',
    "SELECT s.id, s.start_at FROM shifts s WHERE s.status = 'scheduled'",
    'SELECT c.sia_status, c.sia_expiry_date FROM guard_compliance c',
])
def test_expanded_policy_keeps_operational_columns_queryable(sql):
    assert guard().validate(sql).ok


@pytest.mark.parametrize('sql', [
    'SELECT guard_id FROM shifts',
    'SELECT s.id FROM shifts s WHERE s.guard_id IS NULL',
    'SELECT x.guard_id FROM (SELECT guard_id FROM shifts) x',
])
def test_obsolete_shift_columns_are_blocked(sql):
    assert not guard().validate(sql).ok


def test_assignment_columns_remain_available():
    assert guard().validate('SELECT a.guard_id, s.shift_code FROM shift_assignments a JOIN shifts s ON a.shift_id = s.id').ok


def test_guard_assigned_sites_use_shift_site_bridge():
    assert guard().validate("SELECT DISTINCT st.id, st.site FROM guards g JOIN shift_assignments a ON a.guard_id = g.id JOIN shifts s ON a.shift_id = s.id JOIN sites st ON s.site_id = st.id WHERE LOWER(g.first_name) = 'ali'").ok


@pytest.mark.parametrize('sql, expected', [
    ('SELECT id FROM guards', 20),
    ('SELECT id FROM guards LIMIT 100', 20),
    ('SELECT id FROM guards LIMIT 5', 5),
    ('SELECT id FROM guards LIMIT 0', 0),
    ('SELECT id FROM guards LIMIT 100 OFFSET 10', 20),
    ('SELECT id FROM guards UNION ALL SELECT id FROM guards LIMIT 100', 20),
    ('SELECT COUNT(*) AS n FROM guards', 20),
    ('SELECT status, COUNT(*) AS n FROM guards GROUP BY status LIMIT 100', 20),
    ('SELECT id FROM guards LIMIT -1', 20),
])
def test_result_row_cap(sql, expected):
    import sqlglot
    result = guard().validate(sql)
    assert result.ok, result.error
    tree = sqlglot.parse_one(result.sql, read='mysql')
    assert int(tree.args['limit'].expression.this) == expected


def test_settings_cannot_raise_cap():
    from backend.app.config import Settings
    settings = Settings(_env_file=None, default_row_limit=100, max_row_limit=500)
    assert settings.default_row_limit == settings.max_row_limit == 20


def test_execution_fetch_is_bounded(monkeypatch):
    from unittest.mock import MagicMock
    from types import SimpleNamespace
    from backend.app import database
    engine = MagicMock()
    result = engine.connect.return_value.__enter__.return_value.execute.return_value
    result.keys.return_value = ['id']
    result.fetchmany.return_value = [SimpleNamespace(_mapping={'id': i}) for i in range(20)]
    monkeypatch.setattr(database, 'engine', lambda: engine)
    columns, rows = database.execute_select('SELECT id FROM guards LIMIT 20')
    result.fetchmany.assert_called_once_with(20)
    result.fetchall.assert_not_called()
    assert columns == ['id'] and len(rows) == 20
