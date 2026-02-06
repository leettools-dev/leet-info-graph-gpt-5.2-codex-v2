from __future__ import annotations

from pydantic import BaseModel, Field


class SourceCreate(BaseModel):
    """Fields for creating a source."""

    session_id: str
    title: str
    url: str
    snippet: str
    confidence: float


class Source(BaseModel):
    """Source model."""

    source_id: str = Field(..., description="UUID")
    session_id: str
    title: str
    url: str
    snippet: str
    confidence: float
    fetched_at: int
