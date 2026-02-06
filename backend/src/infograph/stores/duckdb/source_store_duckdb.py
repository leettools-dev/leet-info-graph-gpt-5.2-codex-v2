from __future__ import annotations

from dataclasses import dataclass
import time
import uuid

from infograph.core.schemas.source import Source, SourceCreate
from infograph.stores.abstract_source_store import AbstractSourceStore
from infograph.stores.duckdb.duckdb_client import DuckDBClient


@dataclass
class SourceStoreDuckDB(AbstractSourceStore):
    """DuckDB implementation for sources."""

    client: DuckDBClient
    table_name: str = "sources"

    def __post_init__(self) -> None:
        self.client.ensure_table(
            self.table_name,
            """
            CREATE TABLE IF NOT EXISTS sources (
                source_id VARCHAR PRIMARY KEY,
                session_id VARCHAR NOT NULL,
                title VARCHAR NOT NULL,
                url VARCHAR NOT NULL,
                snippet VARCHAR NOT NULL,
                confidence DOUBLE NOT NULL,
                fetched_at BIGINT NOT NULL
            )
            """,
        )

    def create_source(self, source_create: SourceCreate) -> Source:
        source_id = str(uuid.uuid4())
        fetched_at = int(time.time())
        self.client.execute(
            """
            INSERT INTO sources (source_id, session_id, title, url, snippet, confidence, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source_id,
                source_create.session_id,
                source_create.title,
                source_create.url,
                source_create.snippet,
                source_create.confidence,
                fetched_at,
            ),
        )
        return Source(
            source_id=source_id,
            session_id=source_create.session_id,
            title=source_create.title,
            url=source_create.url,
            snippet=source_create.snippet,
            confidence=source_create.confidence,
            fetched_at=fetched_at,
        )

    def list_sources(self, session_id: str) -> list[Source]:
        rows = self.client.fetchall(
            """
            SELECT source_id, session_id, title, url, snippet, confidence, fetched_at
            FROM sources
            WHERE session_id = ?
            ORDER BY fetched_at DESC
            """,
            (session_id,),
        )
        return [self._row_to_source(row) for row in rows if row is not None]

    def delete_sources_for_session(self, session_id: str) -> None:
        self.client.execute("DELETE FROM sources WHERE session_id = ?", (session_id,))

    @staticmethod
    def _row_to_source(row: tuple | None) -> Source | None:
        if row is None:
            return None
        return Source(
            source_id=row[0],
            session_id=row[1],
            title=row[2],
            url=row[3],
            snippet=row[4],
            confidence=row[5],
            fetched_at=row[6],
        )
