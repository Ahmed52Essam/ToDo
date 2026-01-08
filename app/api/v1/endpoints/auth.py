# import logging

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    credentials_exception,
    get_user,
    hash_password,
    verify_password,
)
from app.db.base import User
from app.db.session import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut

# logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=201, response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user(email=user.email, db=db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that email already exists!",
        )
    if user.phone_number:
        query = select(User).where(User.phone_number == user.phone_number)
        if await db.scalar(query):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This phone number is already used!",
            )

    hashed_password = hash_password(user.password)
    new_user = User()
    new_user.email = user.email
    new_user.hashed_password = hashed_password
    new_user.phone_number = user.phone_number
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", status_code=200, response_model=Token)
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
