from fastapi import APIRouter, Request


class APIRouterBase(APIRouter):
    """Base API router with shared helpers."""

    async def get_locale(self, request: Request) -> str:
        """Extract locale from Accept-Language header."""
        accept_language = request.headers.get("Accept-Language", "en-US")
        return accept_language.split(",")[0].strip()
