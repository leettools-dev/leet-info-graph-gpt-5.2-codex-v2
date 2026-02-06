from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException
from pydantic import BaseModel

from infograph.core.schemas.user import User
from infograph.services.auth_service import AuthService, AuthServiceError
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.user_store_duckdb import UserStoreDuckDB
from infograph.svc.api_router_base import APIRouterBase
from infograph.svc.auth import AuthManager, get_auth_manager


class GoogleTokenRequest(BaseModel):
    credential: str


class AuthResponse(BaseModel):
    user: User
    token: str


@dataclass
class AuthRouter(APIRouterBase):
    """Authentication endpoints."""

    auth_service: AuthService
    auth_manager: AuthManager

    def __init__(self) -> None:
        super().__init__()
        user_store = UserStoreDuckDB(client=DuckDBClient(db_name="infograph"))
        self.auth_service = AuthService(user_store=user_store)
        self.auth_manager = get_auth_manager()

        @self.post("/auth/google", response_model=AuthResponse)
        async def google_login(payload: GoogleTokenRequest) -> AuthResponse:
            """Exchange Google credential for JWT token."""
            try:
                google_payload = self.auth_service.verify_google_token(payload.credential)
                user = self.auth_service.get_or_create_user(google_payload)
                token = self.auth_service.issue_token(user)
                return AuthResponse(user=user, token=token)
            except AuthServiceError as exc:
                raise HTTPException(status_code=401, detail=str(exc)) from exc

        @self.get("/auth/me", response_model=User)
        async def get_me(
            calling_user: User = Depends(self.auth_manager.get_user_from_request),
        ) -> User:
            """Return the current authenticated user."""
            return calling_user

        @self.post("/auth/logout")
        async def logout() -> dict:
            """Logout endpoint placeholder."""
            return {"success": True}
