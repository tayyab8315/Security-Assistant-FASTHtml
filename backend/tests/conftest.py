import pytest

@pytest.fixture(autouse=True)
def no_live_database(monkeypatch):
    # Unit tests must not depend on credentials or reach the configured database.
    from backend.app import catalog
    def offline(*args, **kwargs):
        raise RuntimeError('No live database in unit tests')
    monkeypatch.setattr(catalog, 'inspect_live_schema', offline)
