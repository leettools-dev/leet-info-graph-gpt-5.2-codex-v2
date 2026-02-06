from __future__ import annotations

from abc import ABC, abstractmethod

from infograph.core.schemas.source import Source, SourceCreate


class AbstractSourceStore(ABC):
    """Abstract store for sources."""

    @abstractmethod
    def create_source(self, source_create: SourceCreate) -> Source:
        """Create a source."""

    @abstractmethod
    def list_sources(self, session_id: str) -> list[Source]:
        """List sources for a session."""

    @abstractmethod
    def delete_sources_for_session(self, session_id: str) -> None:
        """Delete sources for a session."""
