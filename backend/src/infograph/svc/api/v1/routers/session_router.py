from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from fastapi import Depends, HTTPException
from pydantic import BaseModel

from infograph.core.schemas.message import Message, MessageCreate
from infograph.core.schemas.research_session import (
    ResearchSession,
    ResearchSessionCreate,
)
from infograph.core.schemas.user import User
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.message_store_duckdb import MessageStoreDuckDB
from infograph.stores.duckdb.session_store_duckdb import SessionStoreDuckDB
from infograph.svc.api_router_base import APIRouterBase
from infograph.svc.auth import AuthManager, get_auth_manager


class MessagePayload(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


@dataclass
class SessionRouter(APIRouterBase):
    """Session and message endpoints."""

    session_store: SessionStoreDuckDB
    message_store: MessageStoreDuckDB
    auth_manager: AuthManager

    def __init__(self) -> None:
        super().__init__()
        client = DuckDBClient(db_name="infograph")
        self.session_store = SessionStoreDuckDB(client=client)
        self.message_store = MessageStoreDuckDB(client=client)
        self.auth_manager = get_auth_manager()

        @self.post("/sessions", response_model=ResearchSession)
        async def create_session(
            payload: ResearchSessionCreate,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> ResearchSession:
            """Create a new research session."""
            return self.session_store.create_session(calling_user.user_id, payload)

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
