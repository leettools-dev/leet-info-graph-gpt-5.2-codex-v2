from __future__ import annotations

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Fields for creating a user."""

    email: str
    name: str
    google_id: str


class User(BaseModel):
    """User stored in the system."""

    user_id: str = Field(..., description="UUID")
    email: str
    name: str
    google_id: str
    created_at: int
    updated_at: int
