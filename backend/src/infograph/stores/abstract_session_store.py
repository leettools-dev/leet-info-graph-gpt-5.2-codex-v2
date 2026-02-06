from __future__ import annotations

from abc import ABC, abstractmethod

from infograph.core.schemas.research_session import (
    ResearchSession,
    ResearchSessionCreate,
    ResearchSessionUpdate,
)


class AbstractSessionStore(ABC):
    """Abstract store for research sessions."""

    @abstractmethod
    def create_session(
        self, user_id: str, session_create: ResearchSessionCreate
    ) -> ResearchSession:
        """Create a research session."""

    @abstractmethod
    def get_session(self, session_id: str) -> ResearchSession | None:
        """Fetch a session by ID."""

    @abstractmethod
    def list_sessions(self, user_id: str, limit: int, offset: int) -> list[ResearchSession]:
        """List sessions for a user."""

    @abstractmethod
    def update_session(
        self, session_id: str, session_update: ResearchSessionUpdate
    ) -> ResearchSession | None:
        """Update a session."""

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        """Delete a session."""
