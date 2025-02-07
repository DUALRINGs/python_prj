from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import db_helper, User
from auth.fastapi_users_router import current_user
from . import crud


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    """
    Возвращает пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Пользователь, если найден.
    :raises HTTPException: Если пользователь не найден.
    """
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


async def is_admin_or_owner(
    user: User,
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Проверяет, является ли пользователь администратором или владельцем аккаунта.

    :param user: Пользователь, для которого выполняется проверка.
    :param user_id: Идентификатор пользователя, которого нужно проверить.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если пользователь не имеет прав доступа.
    """
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user",
        )

async def is_superuser(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )