from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from models import helper, User
from . import utils

from .schemas import oauth2_schema




async def user_by_email(session: AsyncSession , email: str) -> User | None:
    """
    Находит пользователя по email.

    :param session: Асинхронная сессия SQLAlchemy.
    :param email: Email пользователя для поиска.
    :return: Объект User, если пользователь найден, иначе None.
    """
    query = select(User).where(User.email == email)
    result: Result = await session.execute(query)
    return result.scalar_one_or_none()

async def validate_auth_user(
    session: AsyncSession = Depends(helper.session_dependency),
    username: str = Form(),
    password: str = Form(),
):

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    if not (user := await user_by_email(session=session, email=username)):
        raise unauthed_exc

    if not utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc


    return user

async def get_current_token_payload(
    token: str = Depends(oauth2_schema),
) -> dict:

    try:
        payload = await utils.decode_jwt(token=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
    return payload

async def get_current_auth_user(
    session: AsyncSession = Depends(helper.session_dependency),
    payload: dict = Depends(get_current_token_payload),
) -> User:

    email: str | None = payload.get("email")
    if user := await user_by_email(session=session, email=email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )