# import logging

from fastapi import APIRouter

# Regestring endpoints
from app.api.v1.endpoints.health import router as health_router

# logger = logging.getLogger(__name__)

api_router = APIRouter()


api_router.include_router(health_router, tags=["health"])
