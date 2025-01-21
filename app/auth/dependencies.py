from typing import Annotated

from fastapi import Path, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from models import helper, User
from . import utils




async def user_by_email(session: AsyncSession , email: str) -> User | None:
    """
    Находит пользователя по email.

    :param session: Асинхронная сессия SQLAlchemy.
    :param email: Email пользователя для поиска.
    :return: Объект User, если пользователь найден, иначе None.
    """
    # Создаем запрос для поиска пользователя по email
    query = select(User).where(User.email == email)
    # Выполняем запрос
    result: Result = await session.execute(query)
    # Возвращаем первый результат (или None, если пользователь не найден)
    return result.scalar_one_or_none()

async def validate_auth_user(
    session: AsyncSession = Depends(helper.session_dependency),
    email: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    if not (user := await user_by_email(session=session, email=email)):
        raise unauthed_exc

    if not utils.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc


    return user