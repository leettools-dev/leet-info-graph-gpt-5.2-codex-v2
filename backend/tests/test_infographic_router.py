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


def test_get_infographic_and_image() -> None:
    client = TestClient(create_app())
    headers, user = _auth_headers()
    session_store = SessionStoreDuckDB(client=DuckDBClient(db_name="infograph"))

    response = client.post(
        "/api/v1/sessions",
        json={"prompt": "Q"},
        headers=headers,
    )
    assert response.status_code == 200
    session_payload = response.json()
    session_id = session_payload["session_id"]

    response = client.get(
        f"/api/v1/sessions/{session_id}/infographic", headers=headers
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == session_id
    assert payload["template_type"] == "basic"

    image_response = client.get(
        f"/api/v1/sessions/{session_id}/infographic/image", headers=headers
    )
    assert image_response.status_code == 200
    assert image_response.headers["content-type"].startswith("image/png")
