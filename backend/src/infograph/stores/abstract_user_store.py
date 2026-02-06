from __future__ import annotations

from abc import ABC, abstractmethod

from infograph.core.schemas.user import User, UserCreate


class AbstractUserStore(ABC):
    """Abstract store for user records."""

    @abstractmethod
    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None:
        """Fetch a user by ID."""

    @abstractmethod
    def get_user_by_google_id(self, google_id: str) -> User | None:
        """Fetch a user by Google ID."""

    @abstractmethod
    def update_user(self, user: User) -> User:
        """Update an existing user."""

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        """Delete a user."""
