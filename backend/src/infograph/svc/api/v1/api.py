from fastapi import APIRouter

from infograph.svc.api.v1.routers.health_router import HealthRouter


class ServiceAPIRouter(APIRouter):
    """Main API router aggregating sub-routers."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        health_router = HealthRouter()
        super().include_router(health_router, tags=["Health"])
