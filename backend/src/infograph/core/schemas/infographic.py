from __future__ import annotations

from pydantic import BaseModel, Field


class InfographicCreate(BaseModel):
    """Fields for creating an infographic."""

    session_id: str
    template_type: str
    layout_data: dict


class Infographic(BaseModel):
    """Infographic model."""

    infographic_id: str = Field(..., description="UUID")
    session_id: str
    image_path: str
    template_type: str
    layout_data: dict
    created_at: int
