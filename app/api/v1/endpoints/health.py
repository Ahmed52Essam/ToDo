# import logging

from fastapi import APIRouter

# logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", status_code=200)
async def get_health():
    return {"status": "ok"}
