from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Any

import duckdb

from infograph.settings import settings


class DuckDBClient:
    """Simple DuckDB client with table creation caching."""

    def __init__(self, db_name: str = "infograph") -> None:
        self.db_name = db_name
        self.db_path = self._get_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._lock = Lock()
        self._table_locks: dict[str, Lock] = {}
        self._created_tables: set[str] = set()

    def _get_db_path(self) -> Path:
        suffix = "_test" if settings.is_test else ""
        return Path(settings.database_path) / f"duckdb_{self.db_name}{suffix}.db"

    def _get_table_lock(self, table_name: str) -> Lock:
        with self._lock:
            if table_name not in self._table_locks:
                self._table_locks[table_name] = Lock()
            return self._table_locks[table_name]

    def execute(self, query: str, parameters: tuple[Any, ...] | None = None) -> None:
        with self.conn.cursor() as cursor:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)

    def fetchone(
        self,
        query: str,
        parameters: tuple[Any, ...] | None = None,
    ) -> tuple[Any, ...] | None:
        with self.conn.cursor() as cursor:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            return cursor.fetchone()

    def fetchall(
        self,
        query: str,
        parameters: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        with self.conn.cursor() as cursor:
            if parameters is None:
                cursor.execute(query)
            else:
                cursor.execute(query, parameters)
            return cursor.fetchall()

    def ensure_table(self, table_name: str, create_sql: str) -> None:
        if table_name in self._created_tables:
            return
        with self._get_table_lock(table_name):
            if table_name in self._created_tables:
                return
            self.execute(create_sql)
            self._created_tables.add(table_name)
