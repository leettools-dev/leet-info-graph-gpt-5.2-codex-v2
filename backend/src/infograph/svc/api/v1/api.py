from fastapi import APIRouter

from infograph.svc.api.v1.routers.auth_router import AuthRouter
from infograph.svc.api.v1.routers.health_router import HealthRouter
from infograph.svc.api.v1.routers.session_router import SessionRouter


class ServiceAPIRouter(APIRouter):
    """Main API router aggregating sub-routers."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        health_router = HealthRouter()
        super().include_router(health_router, tags=["Health"])

        auth_router = AuthRouter()
        super().include_router(auth_router, tags=["Auth"])

        session_router = SessionRouter()
        super().include_router(session_router, tags=["Sessions"])
