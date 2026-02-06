from fastapi.testclient import TestClient

from infograph.svc.api_service import create_app


def test_health_check() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}
