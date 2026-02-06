from __future__ import annotations

from abc import ABC, abstractmethod

from infograph.core.schemas.infographic import Infographic, InfographicCreate


class AbstractInfographicStore(ABC):
    """Abstract store for infographics."""

    @abstractmethod
    def create_infographic(self, infographic_create: InfographicCreate) -> Infographic:
        """Create an infographic."""

    @abstractmethod
    def get_infographic(self, session_id: str) -> Infographic | None:
        """Fetch an infographic for a session."""

    @abstractmethod
    def delete_infographic(self, session_id: str) -> None:
        """Delete infographic for a session."""
