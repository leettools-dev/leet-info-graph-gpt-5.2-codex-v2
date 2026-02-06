from __future__ import annotations

import time
from dataclasses import dataclass

import jwt
from google.auth.transport import requests
from google.oauth2 import id_token

from infograph.core.schemas.user import User, UserCreate
from infograph.settings import settings
from infograph.stores.duckdb.user_store_duckdb import UserStoreDuckDB


class AuthServiceError(RuntimeError):
    """Raised when authentication fails."""


@dataclass
class AuthService:
    """Service for Google OAuth verification and JWT issuance."""

    user_store: UserStoreDuckDB

    def verify_google_token(self, credential: str) -> dict:
        """Verify Google credential and return payload."""
        if not settings.google_client_id:
            raise AuthServiceError("Google client ID not configured")
        try:
            return id_token.verify_oauth2_token(
                credential,
                requests.Request(),
                settings.google_client_id,
            )
        except ValueError as exc:
            raise AuthServiceError("Invalid Google token") from exc

    def get_or_create_user(self, payload: dict) -> User:
        """Fetch existing user or create a new one based on Google payload."""
        google_id = payload.get("sub")
        email = payload.get("email")
        name = payload.get("name") or payload.get("email")
        if not google_id or not email:
            raise AuthServiceError("Google token missing required fields")

        existing_user = self.user_store.get_user_by_google_id(google_id)
        if existing_user:
            return existing_user

        return self.user_store.create_user(
            UserCreate(email=email, name=name, google_id=google_id)
        )

    def issue_token(self, user: User) -> str:
        """Issue JWT token for user."""
        issued_at = int(time.time())
        payload = {
            "sub": user.user_id,
            "email": user.email,
            "name": user.name,
            "iat": issued_at,
            "exp": issued_at + 60 * 60 * 24,
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        """Decode JWT token and return payload."""
        try:
            return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        except jwt.PyJWTError as exc:
            raise AuthServiceError("Invalid token") from exc
