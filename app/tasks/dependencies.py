from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from app.users.schemas import User
from app.models import helper, Task
from . import crud


async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> Task:
    """
    Возвращает задачу по её идентификатору.

    :param task_id: Идентификатор задачи.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Задача, если найдена.
    :raises HTTPException: Если задача не найдена.
    """
    task = await crud.get_task(session=session, task_id=task_id)
    if task:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found!",
    )


async def is_owner(
    user: User,
    task: Task,
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> None:
    """
    Проверяет, является ли пользователь владельцем задачи.

    :param user: Пользователь, для которого выполняется проверка.
    :param task: Задача, владельца которой нужно проверить.
    :param session: Асинхронная сессия SQLAlchemy.
    :raises HTTPException: Если пользователь не является владельцем задачи.
    """
    result: Result = await session.execute(
        select(Task)
        .where(Task.id == task.id)
        .options(selectinload(Task.user))  # Загружаем связанного пользователя
    )
    task_with_user = result.scalar_one_or_none()

    if task_with_user is None or user.id != task_with_user.user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this task!",
        )