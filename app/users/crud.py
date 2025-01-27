from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from app.models import User, Task
from .schemas import UserUpdatePartial
from app.auth.utils import hash_password


async def create_user(
    session: AsyncSession,
    user_in: User,
) -> User:
    """
    Создает нового пользователя.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user_in: Данные для создания пользователя.
    :return: Созданный пользователь.
    """
    # Проверяем, существует ли уже пользователь с таким же email
    stmt = select(User).filter(User.email == user_in.email)
    result = await session.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        # Поднимаем HTTPException с кодом 409 и сообщением
        raise HTTPException(
            status_code=409,
            detail=f"Пользователь с email {user_in.email} уже существует."
        )


async def get_users(
    session: AsyncSession,
) -> list[User]:
    """
    Возвращает список всех пользователей.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список пользователей.
    """
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users = result.scalars().all()
    return list(users)


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> Optional[User]:
    """
    Возвращает пользователя по его идентификатору.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user_id: Идентификатор пользователя.
    :return: Пользователь, если найден, иначе None.
    """
    return await session.get(User, user_id)


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: User | UserUpdatePartial,
    partial: bool = False,
) -> User:
    """
    Обновляет данные пользователя.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Пользователь, данные которого нужно обновить.
    :param user_update: Данные для обновления.
    :param partial: Если True, обновляет только указанные поля.
    :return: Обновленный пользователь.
    """
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    """
    Удаляет пользователя.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Пользователь, которого нужно удалить.
    """
    await session.delete(user)
    await session.commit()