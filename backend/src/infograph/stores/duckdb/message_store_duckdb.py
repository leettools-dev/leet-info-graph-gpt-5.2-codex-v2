from __future__ import annotations

from dataclasses import dataclass
import time
import uuid

from infograph.core.schemas.message import Message, MessageCreate
from infograph.stores.abstract_message_store import AbstractMessageStore
from infograph.stores.duckdb.duckdb_client import DuckDBClient


@dataclass
class MessageStoreDuckDB(AbstractMessageStore):
    """DuckDB implementation for messages."""

    client: DuckDBClient
    table_name: str = "messages"

    def __post_init__(self) -> None:
        self.client.ensure_table(
            self.table_name,
            """
            CREATE TABLE IF NOT EXISTS messages (
                message_id VARCHAR PRIMARY KEY,
                session_id VARCHAR NOT NULL,
                role VARCHAR NOT NULL,
                content VARCHAR NOT NULL,
                created_at BIGINT NOT NULL
            )
            """,
        )

    def create_message(self, message_create: MessageCreate) -> Message:
        message_id = str(uuid.uuid4())
        created_at = int(time.time())
        self.client.execute(
            """
            INSERT INTO messages (message_id, session_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                message_id,
                message_create.session_id,
                message_create.role,
                message_create.content,
                created_at,
            ),
        )
        return Message(
            message_id=message_id,
            session_id=message_create.session_id,
            role=message_create.role,
            content=message_create.content,
            created_at=created_at,
        )

    def list_messages(self, session_id: str) -> list[Message]:
        rows = self.client.fetchall(
            """
            SELECT message_id, session_id, role, content, created_at
            FROM messages
            WHERE session_id = ?
            ORDER BY created_at ASC
            """,
            (session_id,),
        )
        return [self._row_to_message(row) for row in rows if row is not None]

    def delete_messages_for_session(self, session_id: str) -> None:
        self.client.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))

    @staticmethod
    def _row_to_message(row: tuple | None) -> Message | None:
        if row is None:
            return None
        return Message(
            message_id=row[0],
            session_id=row[1],
            role=row[2],
            content=row[3],
            created_at=row[4],
        )
