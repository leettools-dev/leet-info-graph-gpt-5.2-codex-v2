from fastapi.testclient import TestClient

from infograph.svc.api_service import create_app
from infograph.services.auth_service import AuthService
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.user_store_duckdb import UserStoreDuckDB


def test_auth_me_requires_token() -> None:
    client = TestClient(create_app())
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_issue_and_decode_token_round_trip() -> None:
    user_store = UserStoreDuckDB(client=DuckDBClient(db_name="infograph"))
    service = AuthService(user_store=user_store)

    payload = {"sub": "google-123", "email": "user@example.com", "name": "Test User"}
    user = service.get_or_create_user(payload)
    token = service.issue_token(user)
    decoded = service.decode_token(token)

    assert decoded["sub"] == user.user_id
    assert user.email == "user@example.com"
