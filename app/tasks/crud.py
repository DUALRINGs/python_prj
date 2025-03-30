from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from app.models import User, Task
from models import db_helper
from .schemas import TaskUpdatePartial


async def create_task(
    user: User,
    task_in: Task,
    session: AsyncSession,
) -> Task:
    """
    Создает новую задачу для указанного пользователя.

    :param user: Пользователь, для которого создается задача.
    :param task_in: Данные для создания задачи.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Созданная задача.
    """
    task = Task(**task_in.model_dump())
    task.user = user
    session.add(task)
    await session.commit()
    return task

async def get_all_user_tasks(
    session: AsyncSession,
    user: User,
) -> list[Task]:
    """
    Возвращает список задач для указанного пользователя.

    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Пользователь, для которого запрашиваются задачи.
    :return: Список задач.
    """
    statement = select(Task).where(Task.user_id == user.id)
    result: Result = await session.execute(statement)
    tasks = result.scalars().all()
    return list(tasks)

async def get_task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Task:
    """
    Возвращает задачу по её идентификатору.

    :param task_id: Идентификатор задачи.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Задача, если найдена.
    :raises HTTPException: Если задача не найдена.
    """
    task = await session.get(Task, task_id)
    if task:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found!",
    )

async def update_task(
    user: User,
    session: AsyncSession,
    task: Task,
    task_update: Task | TaskUpdatePartial,
    partial: bool = False,
) -> Task:
    """
    Обновляет задачу.

    :param user: Пользователь, который обновляет задачу.
    :param session: Асинхронная сессия SQLAlchemy.
    :param task: Задача, которую нужно обновить.
    :param task_update: Данные для обновления задачи.
    :param partial: Если True, обновляет только указанные поля.
    :return: Обновленная задача.
    """
    for name, value in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, name, value)
    await session.commit()
    return task

async def delete_task(
    session: AsyncSession,
    task: Task,
) -> None:
    """
    Удаляет задачу.

    :param session: Асинхронная сессия SQLAlchemy.
    :param task: Задача, которую нужно удалить.
    """
    await session.delete(task)
    await session.commit()
