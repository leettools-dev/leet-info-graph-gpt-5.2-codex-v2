from __future__ import annotations

from dataclasses import dataclass
import time
import uuid

from infograph.core.schemas.user import User, UserCreate
from infograph.stores.abstract_user_store import AbstractUserStore
from infograph.stores.duckdb.duckdb_client import DuckDBClient


@dataclass
class UserStoreDuckDB(AbstractUserStore):
    """DuckDB implementation for users."""

    client: DuckDBClient
    table_name: str = "users"

    def __post_init__(self) -> None:
        self.client.ensure_table(
            self.table_name,
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR PRIMARY KEY,
                email VARCHAR NOT NULL,
                name VARCHAR NOT NULL,
                google_id VARCHAR NOT NULL,
                created_at BIGINT NOT NULL,
                updated_at BIGINT NOT NULL
            )
            """,
        )

    def create_user(self, user_create: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        timestamp = int(time.time())
        self.client.execute(
            """
            INSERT INTO users (user_id, email, name, google_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, user_create.email, user_create.name, user_create.google_id, timestamp, timestamp),
        )
        return User(
            user_id=user_id,
            email=user_create.email,
            name=user_create.name,
            google_id=user_create.google_id,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def get_user_by_id(self, user_id: str) -> User | None:
        row = self.client.fetchone(
            """
            SELECT user_id, email, name, google_id, created_at, updated_at
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        )
        return self._row_to_user(row)

    def get_user_by_google_id(self, google_id: str) -> User | None:
        row = self.client.fetchone(
            """
            SELECT user_id, email, name, google_id, created_at, updated_at
            FROM users
            WHERE google_id = ?
            """,
            (google_id,),
        )
        return self._row_to_user(row)

    def update_user(self, user: User) -> User:
        updated_at = int(time.time())
        self.client.execute(
            """
            UPDATE users
            SET email = ?, name = ?, google_id = ?, updated_at = ?
            WHERE user_id = ?
            """,
            (user.email, user.name, user.google_id, updated_at, user.user_id),
        )
        return User(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            google_id=user.google_id,
            created_at=user.created_at,
            updated_at=updated_at,
        )

    def delete_user(self, user_id: str) -> None:
        self.client.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    @staticmethod
    def _row_to_user(row: tuple | None) -> User | None:
        if row is None:
            return None
        return User(
            user_id=row[0],
            email=row[1],
            name=row[2],
            google_id=row[3],
            created_at=row[4],
            updated_at=row[5],
        )
