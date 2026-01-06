# import logging


from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.db.base import User
from app.schemas.user import UserOut

# logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
