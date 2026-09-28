from starlette.testclient import TestClient

from backend.app.main import app


def test_api_starts_and_health_responds():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
