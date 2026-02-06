from fastapi.testclient import TestClient

from infograph.core.schemas.message import MessageCreate
from infograph.core.schemas.research_session import ResearchSessionCreate
from infograph.core.schemas.user import User
from infograph.services.auth_service import AuthService
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.message_store_duckdb import MessageStoreDuckDB
from infograph.stores.duckdb.session_store_duckdb import SessionStoreDuckDB
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


def test_session_crud_and_messages() -> None:
    client = TestClient(create_app())
    headers, user = _auth_headers()

    create_payload = {"prompt": "Explain renewable energy trends"}
    response = client.post("/api/v1/sessions", json=create_payload, headers=headers)

    assert response.status_code == 200
    session = response.json()
    assert session["prompt"] == create_payload["prompt"]
    assert session["user_id"] == user.user_id

    list_response = client.get("/api/v1/sessions", headers=headers)
    assert list_response.status_code == 200
    sessions = list_response.json()
    assert any(item["session_id"] == session["session_id"] for item in sessions)

    get_response = client.get(
        f"/api/v1/sessions/{session['session_id']}", headers=headers
    )
    assert get_response.status_code == 200

    message_payload = {"role": "user", "content": "Give me key stats"}
    message_response = client.post(
        f"/api/v1/sessions/{session['session_id']}/messages",
        json=message_payload,
        headers=headers,
    )
    assert message_response.status_code == 200
    message = message_response.json()
    assert message["content"] == message_payload["content"]

    messages_response = client.get(
        f"/api/v1/sessions/{session['session_id']}/messages", headers=headers
    )
    assert messages_response.status_code == 200
    messages = messages_response.json()
    assert len(messages) == 1

    delete_response = client.delete(
        f"/api/v1/sessions/{session['session_id']}", headers=headers
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {"success": True}

    store_session = SessionStoreDuckDB(client=DuckDBClient(db_name="infograph"))
    assert store_session.get_session(session["session_id"]) is None

    store_messages = MessageStoreDuckDB(client=DuckDBClient(db_name="infograph"))
    assert store_messages.list_messages(session["session_id"]) == []


def test_message_requires_authorized_session() -> None:
    client = TestClient(create_app())
    headers, _ = _auth_headers()

    response = client.post(
        "/api/v1/sessions/bad-session/messages",
        json={"role": "user", "content": "Hello"},
        headers=headers,
    )

    assert response.status_code == 404
