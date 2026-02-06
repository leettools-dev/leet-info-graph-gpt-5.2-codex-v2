from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """Fields for creating a message."""

    session_id: str
    role: Literal["user", "assistant", "system"]
    content: str


class Message(BaseModel):
    """Message model."""

    message_id: str = Field(..., description="UUID")
    session_id: str
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: int
