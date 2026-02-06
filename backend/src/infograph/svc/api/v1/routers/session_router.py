from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from fastapi import Depends, HTTPException
from pydantic import BaseModel

from infograph.core.schemas.message import Message, MessageCreate
from infograph.core.schemas.research_session import (
    ResearchSession,
    ResearchSessionCreate,
    ResearchSessionUpdate,
)
from infograph.core.schemas.user import User
from infograph.services.infographic_service import (
    InfographicService,
    InfographicServiceError,
)
from infograph.services.search_service import SearchService, SearchServiceError
from infograph.settings import settings
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.infographic_store_duckdb import InfographicStoreDuckDB
from infograph.stores.duckdb.message_store_duckdb import MessageStoreDuckDB
from infograph.stores.duckdb.session_store_duckdb import SessionStoreDuckDB
from infograph.stores.duckdb.source_store_duckdb import SourceStoreDuckDB
from infograph.svc.api_router_base import APIRouterBase
from infograph.svc.auth import AuthManager, get_auth_manager


TEST_SEARCH_HTML = """
<html>
<body>
  <div class="results">
    <a class="result__a" href="https://example.com/alpha">Alpha Title</a>
    <span class="result__snippet">Alpha snippet text.</span>
  </div>
  <div class="results">
    <a class="result__a" href="/beta">Beta Title</a>
    <span class="result__snippet">Beta snippet text.</span>
  </div>
</body>
</html>
"""


class MessagePayload(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


@dataclass
class SessionRouter(APIRouterBase):
    """Session and message endpoints."""

    session_store: SessionStoreDuckDB
    message_store: MessageStoreDuckDB
    source_store: SourceStoreDuckDB
    infographic_store: InfographicStoreDuckDB
    auth_manager: AuthManager
    search_service: SearchService
    infographic_service: InfographicService

    def __init__(self) -> None:
        super().__init__()
        client = DuckDBClient(db_name="infograph")
        self.session_store = SessionStoreDuckDB(client=client)
        self.message_store = MessageStoreDuckDB(client=client)
        self.source_store = SourceStoreDuckDB(client=client)
        self.infographic_store = InfographicStoreDuckDB(client=client)
        self.auth_manager = get_auth_manager()
        test_fetcher = (lambda _query: TEST_SEARCH_HTML) if settings.is_test else None
        self.search_service = SearchService(fetcher=test_fetcher)
        self.infographic_service = InfographicService(
            infographic_store=self.infographic_store,
        )

        @self.post("/sessions", response_model=ResearchSession)
        async def create_session(
            payload: ResearchSessionCreate,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> ResearchSession:
            """Create a new research session."""
            session = self.session_store.create_session(calling_user.user_id, payload)
            self.session_store.update_session(
                session.session_id,
                ResearchSessionUpdate(status="searching"),
            )
            try:
                sources = self.search_service.search_sources(
                    session.session_id,
                    session.prompt,
                )
                for source in sources:
                    self.source_store.create_source(source)
                self.session_store.update_session(
                    session.session_id,
                    ResearchSessionUpdate(status="generating"),
                )
                stored_sources = self.source_store.list_sources(session.session_id)
                session = self.session_store.get_session(session.session_id) or session
                try:
                    self.infographic_service.generate_infographic(
                        session=session,
                        sources=stored_sources,
                    )
                except InfographicServiceError as exc:
                    self.session_store.update_session(
                        session.session_id,
                        ResearchSessionUpdate(status="failed"),
                    )
                    raise HTTPException(
                        status_code=500, detail="Infographic generation failed"
                    ) from exc

                updated = self.session_store.update_session(
                    session.session_id,
                    ResearchSessionUpdate(status="completed"),
                )
                return updated or session
            except SearchServiceError as exc:
                self.session_store.update_session(
                    session.session_id,
                    ResearchSessionUpdate(status="failed"),
                )
                raise HTTPException(
                    status_code=502, detail="Search request failed"
                ) from exc

        @self.get("/sessions", response_model=list[ResearchSession])
        async def list_sessions(
            limit: int = 10,
            offset: int = 0,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> list[ResearchSession]:
            """List research sessions for the authenticated user."""
            return self.session_store.list_sessions(calling_user.user_id, limit, offset)

        @self.get("/sessions/{session_id}", response_model=ResearchSession)
        async def get_session(
            session_id: str,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> ResearchSession:
            """Get a research session by ID."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            return session

        @self.delete("/sessions/{session_id}")
        async def delete_session(
            session_id: str,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> dict:
            """Delete a research session."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            self.message_store.delete_messages_for_session(session_id)
            self.source_store.delete_sources_for_session(session_id)
            self.infographic_store.delete_infographic(session_id)
            self.session_store.delete_session(session_id)
            return {"success": True}

        @self.post("/sessions/{session_id}/messages", response_model=Message)
        async def create_message(
            session_id: str,
            payload: MessagePayload,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> Message:
            """Create a message in a session."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            message_create = MessageCreate(
                session_id=session_id,
                role=payload.role,
                content=payload.content,
            )
            return self.message_store.create_message(message_create)

        @self.get("/sessions/{session_id}/messages", response_model=list[Message])
        async def list_messages(
            session_id: str,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> list[Message]:
            """List messages for a session."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            return self.message_store.list_messages(session_id)
