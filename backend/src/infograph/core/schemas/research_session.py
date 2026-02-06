from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ResearchSessionCreate(BaseModel):
    """Fields for creating a research session."""

    prompt: str


class ResearchSession(BaseModel):
    """Research session model."""

    session_id: str = Field(..., description="UUID")
    user_id: str
    prompt: str
    status: Literal["pending", "searching", "generating", "completed", "failed"]
    created_at: int
    updated_at: int


class ResearchSessionUpdate(BaseModel):
    """Fields for updating a research session."""

    status: Literal["pending", "searching", "generating", "completed", "failed"] | None = None
