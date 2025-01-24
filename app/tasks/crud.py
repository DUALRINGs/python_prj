from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from fastapi import Depends

from models import User, Task
from .schemas import TaskUpdatePartial, TaskResponse
from auth.dependencies import get_current_auth_user


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


async def get_tasks(
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


async def get_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    """
    Возвращает задачу по её идентификатору.

    :param session: Асинхронная сессия SQLAlchemy.
    :param task_id: Идентификатор задачи.
    :return: Задача, если найдена, иначе None.
    """
    return await session.get(Task, task_id)


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