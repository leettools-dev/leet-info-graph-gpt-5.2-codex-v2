from __future__ import annotations

from dataclasses import dataclass
import time
import uuid

from infograph.core.schemas.infographic import Infographic, InfographicCreate
from infograph.stores.abstract_infographic_store import AbstractInfographicStore
from infograph.stores.duckdb.duckdb_client import DuckDBClient


@dataclass
class InfographicStoreDuckDB(AbstractInfographicStore):
    """DuckDB implementation for infographics."""

    client: DuckDBClient
    table_name: str = "infographics"

    def __post_init__(self) -> None:
        self.client.ensure_table(
            self.table_name,
            """
            CREATE TABLE IF NOT EXISTS infographics (
                infographic_id VARCHAR PRIMARY KEY,
                session_id VARCHAR NOT NULL,
                image_path VARCHAR NOT NULL,
                template_type VARCHAR NOT NULL,
                layout_data JSON NOT NULL,
                created_at BIGINT NOT NULL
            )
            """,
        )

    def create_infographic(self, infographic_create: InfographicCreate) -> Infographic:
        infographic_id = str(uuid.uuid4())
        created_at = int(time.time())
        self.client.execute(
            """
            INSERT INTO infographics (infographic_id, session_id, image_path, template_type, layout_data, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                infographic_id,
                infographic_create.session_id,
                infographic_create.layout_data.get("image_path", ""),
                infographic_create.template_type,
                infographic_create.layout_data,
                created_at,
            ),
        )
        return Infographic(
            infographic_id=infographic_id,
            session_id=infographic_create.session_id,
            image_path=infographic_create.layout_data.get("image_path", ""),
            template_type=infographic_create.template_type,
            layout_data=infographic_create.layout_data,
            created_at=created_at,
        )

    def get_infographic(self, session_id: str) -> Infographic | None:
        row = self.client.fetchone(
            """
            SELECT infographic_id, session_id, image_path, template_type, layout_data, created_at
            FROM infographics
            WHERE session_id = ?
            """,
            (session_id,),
        )
        return self._row_to_infographic(row)

    def delete_infographic(self, session_id: str) -> None:
        self.client.execute("DELETE FROM infographics WHERE session_id = ?", (session_id,))

    @staticmethod
    def _row_to_infographic(row: tuple | None) -> Infographic | None:
        if row is None:
            return None
        return Infographic(
            infographic_id=row[0],
            session_id=row[1],
            image_path=row[2],
            template_type=row[3],
            layout_data=row[4],
            created_at=row[5],
        )
