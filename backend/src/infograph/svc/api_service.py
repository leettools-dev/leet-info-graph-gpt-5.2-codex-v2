from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infograph.svc.api.v1.api import ServiceAPIRouter


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Infograph API",
        description="Research Infograph Assistant API",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_router = ServiceAPIRouter()
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()


class APIService:
    """Wrapper for running the API service."""

    def __init__(self, app_instance: FastAPI | None = None) -> None:
        self.app = app_instance or create_app()

    def run(self, host: str, port: int) -> None:
        import uvicorn

        uvicorn.run(self.app, host=host, port=port)
