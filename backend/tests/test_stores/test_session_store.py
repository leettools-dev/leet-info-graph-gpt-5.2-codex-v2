from infograph.core.schemas.research_session import ResearchSessionCreate, ResearchSessionUpdate
from infograph.stores.duckdb.session_store_duckdb import SessionStoreDuckDB


def test_session_store_crud(duckdb_client) -> None:
    store = SessionStoreDuckDB(client=duckdb_client)
    session = store.create_session(
        user_id="user-1",
        session_create=ResearchSessionCreate(prompt="Test prompt"),
    )

    fetched = store.get_session(session.session_id)
    assert fetched is not None
    assert fetched.prompt == "Test prompt"

    sessions = store.list_sessions(user_id="user-1", limit=10, offset=0)
    assert len(sessions) == 1

    updated = store.update_session(
        session.session_id,
        ResearchSessionUpdate(status="completed"),
    )
    assert updated is not None
    assert updated.status == "completed"

    store.delete_session(session.session_id)
    assert store.get_session(session.session_id) is None
