from typing import Annotated, Optional

from fastapi import Path, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from app.models import helper, User
from . import utils
from .schemas import oauth2_schema


async def user_by_email(session: AsyncSession, email: str) -> Optional[User]:
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
    email: str = Form(),
    password: str = Form(),
) -> User:
    """
    Проверяет аутентификационные данные пользователя.

    :param session: Асинхронная сессия SQLAlchemy.
    :param email: Имя пользователя (email) для проверки.
    :param password: Пароль для проверки.
    :return: Объект User, если аутентификация успешна.
    :raises HTTPException: Если аутентификация не удалась.
    """
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )
    if not (user := await user_by_email(session=session, email=email)):
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
    """
    Декодирует JWT-токен и возвращает его payload.

    :param token: JWT-токен.
    :return: Payload токена.
    :raises HTTPException: Если токен недействителен.
    """
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
    """
    Возвращает текущего аутентифицированного пользователя на основе payload токена.

    :param session: Асинхронная сессия SQLAlchemy.
    :param payload: Payload JWT-токена.
    :return: Объект User, если пользователь найден.
    :raises HTTPException: Если пользователь не найден.
    """
    email: Optional[str] = payload.get("email")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload does not contain email",
        )

    if user := await user_by_email(session=session, email=email):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found)",
    )