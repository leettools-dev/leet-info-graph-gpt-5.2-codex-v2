import os

from pydantic import BaseModel, Field


def _get_env(key: str, default: str) -> str:
    return os.getenv(key, default)


class SystemSettings(BaseModel):
    """Application settings loaded from environment."""

    database_path: str = Field(
        default_factory=lambda: _get_env("DATABASE_PATH", "/workspace/data/duckdb"),
        description="Directory for DuckDB database files",
    )
    infographic_path: str = Field(
        default_factory=lambda: _get_env("INFOGRAPHIC_PATH", "/workspace/data/infographics"),
        description="Directory for infographic image storage",
    )
    jwt_secret: str = Field(
        default_factory=lambda: _get_env("JWT_SECRET", "change-me"),
        description="JWT signing secret",
    )
    google_client_id: str = Field(
        default_factory=lambda: _get_env("GOOGLE_CLIENT_ID", ""),
        description="Google OAuth client ID",
    )
    log_level: str = Field(
        default_factory=lambda: _get_env("LOG_LEVEL", "info"),
        description="Log level",
    )
    is_test: bool = Field(False, description="Whether running in test mode")


settings = SystemSettings()
