import datetime
from typing import Literal

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.db.base import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email: str):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    jwt_data = {"sub": email, "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(
        jwt_data, key=config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


def get_subject_for_token_type(
    token: str, type: Literal["access", "confirmation"]
) -> str:
    try:
        payload = jwt.decode(
            token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
    except ExpiredSignatureError as e:
        raise credentials_exception("Token has expired!") from e
    except JWTError as e:
        raise credentials_exception("Invalid token!") from e

    email = payload.get("sub")
    if email is None:
        raise credentials_exception("Token is missing 'sub' field")

    token_type = payload.get("type")
    if token_type is None or token_type != type:
        raise credentials_exception(f"Token has incorrect type , expected '{type}'")

    return email


async def get_user(email: EmailStr, db: AsyncSession) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.scalar(query)
    if result:
        return result
    else:
        return None


async def get_user_by_phone(phone_number: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.phone_number == phone_number)
    result = await db.scalar(query)
    if result:
        return result
    else:
        return None


def credentials_exception(exception_details: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=exception_details,
        headers={"WWW-Authenticate": "Bearer"},
    )
