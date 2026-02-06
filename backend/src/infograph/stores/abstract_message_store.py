from __future__ import annotations

from abc import ABC, abstractmethod

from infograph.core.schemas.message import Message, MessageCreate


class AbstractMessageStore(ABC):
    """Abstract store for messages."""

    @abstractmethod
    def create_message(self, message_create: MessageCreate) -> Message:
        """Create a message."""

    @abstractmethod
    def list_messages(self, session_id: str) -> list[Message]:
        """List messages for a session."""

    @abstractmethod
    def delete_messages_for_session(self, session_id: str) -> None:
        """Delete messages for a session."""
