# import logging

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

# logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/db-ping", status_code=200)
async def db_ping(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"db": "ok"}
