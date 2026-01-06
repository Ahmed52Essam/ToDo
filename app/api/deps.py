from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.core.security import (
    credentials_exception,
    get_subject_for_token_type,
    get_user,
)
from app.db.session import get_db

oauth2scheme = OAuth2PasswordBearer(tokenUrl=f"{config.API_V1_PREFIX}/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2scheme)], db: AsyncSession = Depends(get_db)
):
    email = get_subject_for_token_type(token, "access")
    user = await get_user(email, db=db)
    if user is None:
        raise credentials_exception("Could not find user for this token")
    return user
