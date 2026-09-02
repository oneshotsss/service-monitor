from fastapi import APIRouter

from app.api.endpoints.health import router as health_router
from app.api.endpoints.services import router as services_router
from app.api.endpoints.heartbeat import router as heartbeat_router
from app.api.endpoints.services_detail import router as services_detail_router
from app.api.endpoints.frontend import router as frontend_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(services_router)
api_router.include_router(heartbeat_router)
api_router.include_router(services_detail_router)
# frontend templates and static
api_router.include_router(frontend_router)
