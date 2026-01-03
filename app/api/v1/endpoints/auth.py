# import logging

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hashed, verify_password
from app.db.base import User
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut

# logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/signup", status_code=201, response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user(email=user.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that email already exists!",
        )
    hashed_password = get_password_hashed(user.password)
    new_user = User()
    new_user.email = user.email
    new_user.hashed_password = hashed_password
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", status_code=201, response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    # form_data.username is email as the user sents email
    user = await get_user(email=form_data.username, db=db)
    if not user:
        raise credentials_exception("Invalid email or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise credentials_exception("Invalid email or password")
    # if not user.confirmed:
    #     raise credentials_exception("User has not confirmed email")
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


async def get_user(email: EmailStr, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.scalar(query)
    if result:
        return result


def credentials_exception(exception_details: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exception_details,
        headers={"WWW-Authenticate": "Bearer"},
    )
