from __future__ import annotations

from dataclasses import dataclass
import time
import uuid

from infograph.core.schemas.research_session import (
    ResearchSession,
    ResearchSessionCreate,
    ResearchSessionUpdate,
)
from infograph.stores.abstract_session_store import AbstractSessionStore
from infograph.stores.duckdb.duckdb_client import DuckDBClient


@dataclass
class SessionStoreDuckDB(AbstractSessionStore):
    """DuckDB implementation for sessions."""

    client: DuckDBClient
    table_name: str = "research_sessions"

    def __post_init__(self) -> None:
        self.client.ensure_table(
            self.table_name,
            """
            CREATE TABLE IF NOT EXISTS research_sessions (
                session_id VARCHAR PRIMARY KEY,
                user_id VARCHAR NOT NULL,
                prompt VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                created_at BIGINT NOT NULL,
                updated_at BIGINT NOT NULL
            )
            """,
        )

    def create_session(
        self, user_id: str, session_create: ResearchSessionCreate
    ) -> ResearchSession:
        session_id = str(uuid.uuid4())
        timestamp = int(time.time())
        status = "pending"
        self.client.execute(
            """
            INSERT INTO research_sessions (session_id, user_id, prompt, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (session_id, user_id, session_create.prompt, status, timestamp, timestamp),
        )
        return ResearchSession(
            session_id=session_id,
            user_id=user_id,
            prompt=session_create.prompt,
            status=status,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get_session(self, session_id: str) -> ResearchSession | None:
        row = self.client.fetchone(
            """
            SELECT session_id, user_id, prompt, status, created_at, updated_at
            FROM research_sessions
            WHERE session_id = ?
            """,
            (session_id,),
        )
        return self._row_to_session(row)

    def list_sessions(self, user_id: str, limit: int, offset: int) -> list[ResearchSession]:
        rows = self.client.fetchall(
            """
            SELECT session_id, user_id, prompt, status, created_at, updated_at
            FROM research_sessions
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset),
        )
        return [self._row_to_session(row) for row in rows if row is not None]

    def update_session(
        self, session_id: str, session_update: ResearchSessionUpdate
    ) -> ResearchSession | None:
        existing = self.get_session(session_id)
        if existing is None:
            return None
        status = session_update.status or existing.status
        updated_at = int(time.time())
        self.client.execute(
            """
            UPDATE research_sessions
            SET status = ?, updated_at = ?
            WHERE session_id = ?
            """,
            (status, updated_at, session_id),
        )
        return ResearchSession(
            session_id=existing.session_id,
            user_id=existing.user_id,
            prompt=existing.prompt,
            status=status,
            created_at=existing.created_at,
            updated_at=updated_at,
        )

    def delete_session(self, session_id: str) -> None:
        self.client.execute("DELETE FROM research_sessions WHERE session_id = ?", (session_id,))

    @staticmethod
    def _row_to_session(row: tuple | None) -> ResearchSession | None:
        if row is None:
            return None
        return ResearchSession(
            session_id=row[0],
            user_id=row[1],
            prompt=row[2],
            status=row[3],
            created_at=row[4],
            updated_at=row[5],
        )
