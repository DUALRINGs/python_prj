from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from app.schemas.users import BaseUser
from app.models import db_helper, Task


async def is_owner_or_superuser(
    user: BaseUser,
    task: Task,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Проверяет, является ли пользователь владельцем задачи.

    :param user: Пользователь, для которого выполняется проверка.
    :param task: Задача, владельца которой нужно проверить.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если пользователь не является владельцем задачи.
    """
    if user.is_superuser:
        return

    result: Result = await session.execute(
        select(Task)
        .where(Task.id == task.id)
        .options(selectinload(Task.user))  # Загружаем связанного пользователя
    )
    task_with_user = result.scalar_one_or_none()

    if task_with_user is None or user.id != task_with_user.user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this task or a superuser!",
        )
