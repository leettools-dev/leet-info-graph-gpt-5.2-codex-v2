from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse

from infograph.core.schemas.infographic import Infographic
from infograph.core.schemas.user import User
from infograph.services.infographic_service import InfographicService
from infograph.settings import settings
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.infographic_store_duckdb import InfographicStoreDuckDB
from infograph.stores.duckdb.session_store_duckdb import SessionStoreDuckDB
from infograph.svc.api_router_base import APIRouterBase
from infograph.svc.auth import AuthManager, get_auth_manager


@dataclass
class InfographicRouter(APIRouterBase):
    """Infographic endpoints."""

    session_store: SessionStoreDuckDB
    infographic_store: InfographicStoreDuckDB
    auth_manager: AuthManager
    infographic_service: InfographicService

    def __init__(self) -> None:
        super().__init__()
        client = DuckDBClient(db_name="infograph")
        self.session_store = SessionStoreDuckDB(client=client)
        self.infographic_store = InfographicStoreDuckDB(client=client)
        self.auth_manager = get_auth_manager()
        self.infographic_service = InfographicService(
            infographic_store=self.infographic_store,
            output_dir=Path(settings.infographic_path),
        )

        @self.get("/sessions/{session_id}/infographic", response_model=Infographic)
        async def get_infographic(
            session_id: str,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> Infographic:
            """Get infographic metadata for a session."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            infographic = self.infographic_service.get_infographic(session_id)
            if infographic is None:
                raise HTTPException(status_code=404, detail="Infographic not found")
            return infographic

        @self.get("/sessions/{session_id}/infographic/image")
        async def get_infographic_image(
            session_id: str,
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> FileResponse:
            """Return the infographic image file."""
            session = self.session_store.get_session(session_id)
            if session is None:
                raise HTTPException(status_code=404, detail="Session not found")
            if session.user_id != calling_user.user_id:
                raise HTTPException(status_code=403, detail="Not authorized")
            infographic = self.infographic_service.get_infographic(session_id)
            if infographic is None:
                raise HTTPException(status_code=404, detail="Infographic not found")
            image_path = Path(infographic.image_path)
            if not image_path.exists():
                raise HTTPException(status_code=404, detail="Image not found")
            return FileResponse(
                image_path,
                media_type="image/png",
                filename=image_path.name,
            )
