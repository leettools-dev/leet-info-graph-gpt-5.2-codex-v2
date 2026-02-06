from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer_scheme = HTTPBearer(auto_error=False)

from infograph.core.schemas.user import User
from infograph.services.auth_service import AuthService, AuthServiceError
from infograph.stores.duckdb.duckdb_client import DuckDBClient
from infograph.stores.duckdb.user_store_duckdb import UserStoreDuckDB


@dataclass
class AuthManager:
    """Authentication dependency provider."""

    auth_service: AuthService

    def get_user_from_request(
        self,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
    ) -> User:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Missing token")
        try:
            payload = self.auth_service.decode_token(credentials.credentials)
        except AuthServiceError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = self.auth_service.user_store.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user


def get_auth_manager() -> AuthManager:
    user_store = UserStoreDuckDB(client=DuckDBClient(db_name="infograph"))
    auth_service = AuthService(user_store=user_store)
    return AuthManager(auth_service=auth_service)
