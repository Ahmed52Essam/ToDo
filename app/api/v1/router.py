# import logging

from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.db_ping import router as db_router

# Regestring endpoints
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.tasks import router as task_router
from app.api.v1.endpoints.users import router as user_router

# logger = logging.getLogger(__name__)

api_router = APIRouter()


api_router.include_router(health_router)
api_router.include_router(db_router)
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(task_router)
