from pydantic import BaseModel, Field


class SystemSettings(BaseModel):
    """Application settings loaded from environment."""

    database_path: str = Field(
        "/workspace/data/duckdb",
        description="Directory for DuckDB database files",
    )
    infographic_path: str = Field(
        "/workspace/data/infographics",
        description="Directory for infographic image storage",
    )
    jwt_secret: str = Field("change-me", description="JWT signing secret")
    google_client_id: str = Field("", description="Google OAuth client ID")
    log_level: str = Field("info", description="Log level")
    is_test: bool = Field(False, description="Whether running in test mode")


settings = SystemSettings()
