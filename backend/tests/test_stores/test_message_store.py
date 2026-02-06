from infograph.core.schemas.message import MessageCreate
from infograph.stores.duckdb.message_store_duckdb import MessageStoreDuckDB


def test_message_store_crud(duckdb_client) -> None:
    store = MessageStoreDuckDB(client=duckdb_client)
    message = store.create_message(
        MessageCreate(session_id="session-1", role="user", content="Hello")
    )

    messages = store.list_messages("session-1")
    assert len(messages) == 1
    assert messages[0].message_id == message.message_id

    store.delete_messages_for_session("session-1")
    assert store.list_messages("session-1") == []
