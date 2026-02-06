from __future__ import annotations

from fastapi.testclient import TestClient

from infograph.core.schemas.user import User
from infograph.services.auth_service import AuthService
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.user_store_duckdb import UserStoreDuckDB
from infograph.svc.api_service import create_app


def _auth_headers() -> tuple[dict[str, str], User]:
    user_store = UserStoreDuckDB(client=DuckDBClient(db_name="infograph"))
    auth_service = AuthService(user_store=user_store)
    user = auth_service.get_or_create_user(
        {"sub": "google-123", "email": "test@example.com", "name": "Tester"}
    )
    token = auth_service.issue_token(user)
    return {"Authorization": f"Bearer {token}"}, user


def test_list_sources_for_session() -> None:
    client = TestClient(create_app())
    headers, _ = _auth_headers()

    response = client.post(
        "/api/v1/sessions",
        json={"prompt": "Explain renewable energy"},
        headers=headers,
    )
    assert response.status_code == 200
    session_id = response.json()["session_id"]

    sources_response = client.get(
        f"/api/v1/sessions/{session_id}/sources", headers=headers
    )
    assert sources_response.status_code == 200
    sources = sources_response.json()
    assert len(sources) >= 1
    assert all(source["session_id"] == session_id for source in sources)


def test_sources_require_authorized_session() -> None:
    client = TestClient(create_app())
    headers, _ = _auth_headers()

    response = client.get("/api/v1/sessions/missing/sources", headers=headers)

    assert response.status_code == 404
