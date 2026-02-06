from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException

from infograph.core.schemas.source import Source
from infograph.core.schemas.user import User
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.session_store_duckdb import SessionStoreDuckDB
from infograph.stores.duckdb.source_store_duckdb import SourceStoreDuckDB
from infograph.svc.api_router_base import APIRouterBase
from infograph.svc.auth import AuthManager, get_auth_manager


@dataclass
class SourceRouter(APIRouterBase):
    """Source endpoints."""

    session_store: SessionStoreDuckDB
    source_store: SourceStoreDuckDB
    auth_manager: AuthManager

    def __init__(self) -> None:
        super().__init__()
        client = DuckDBClient(db_name="infograph")
        self.session_store = SessionStoreDuckDB(client=client)
        self.source_store = SourceStoreDuckDB(client=client)
        self.auth_manager = get_auth_manager()

        @self.get("/sessions/{session_id}/sources", response_model=list[Source])
        async def list_sources(
            session_id: str,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> list[Source]:
            """List sources for a research session."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            return self.source_store.list_sources(session_id)
