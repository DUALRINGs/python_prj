from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks import crud
from app.models import db_helper
from .schemas import Task, TaskUpdatePartial, TaskResponse
from app.users.schemas import User
from .dependencies import task_by_id, is_owner

router = APIRouter(prefix="/task", tags=["Tasks"])


@router.get("/", response_model=list[Task])
async def get_tasks(
    user: User,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> list[Task]:
    """
    Возвращает список задач для текущего пользователя.

    :param user: Текущий аутентифицированный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список задач.
    """
    return await crud.get_tasks(session=session, user=user)


@router.get("/{task_id}", response_model=Task)
async def get_task_by_id(
    task: Task = Depends(task_by_id),
) -> Task:
    """
    Возвращает задачу по её идентификатору.

    :param task: Задача, найденная по идентификатору.
    :return: Задача.
    """
    return task


@router.post("/", response_model=Task)
async def create_task(
    task_in: Task,
    user: User,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Task:
    """
    Создает новую задачу для текущего пользователя.

    :param task_in: Данные для создания задачи.
    :param user: Текущий аутентифицированный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Созданная задача.
    """
    return await crud.create_task(user=user, session=session, task_in=task_in)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_update: TaskUpdatePartial,
    user: User,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TaskResponse:
    """
    Полностью обновляет задачу.

    :param task_update: Данные для обновления задачи.
    :param user: Текущий аутентифицированный пользователь.
    :param task: Задача, которую нужно обновить.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Обновленная задача.
    """
    await is_owner(user=user, task=task, session=session)
    updated_task = await crud.update_task(
        user=user,
        session=session,
        task=task,
        task_update=task_update,
    )
    return updated_task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_partial_endpoint(
    task_update: TaskUpdatePartial,
    user: User,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TaskResponse:
    """
    Частично обновляет задачу.

    :param task_update: Данные для обновления задачи.
    :param user: Текущий аутентифицированный пользователь.
    :param task: Задача, которую нужно обновить.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Обновленная задача.
    """
    await is_owner(user=user, task=task, session=session)
    updated_task = await crud.update_task(
        user=user,
        session=session,
        task=task,
        task_update=task_update,
        partial=True,
    )
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user: User,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Удаляет задачу.

    :param user: Текущий аутентифицированный пользователь.
    :param task: Задача, которую нужно удалить.
    :param session: Асинхронная сессия SQLAlchemy.
    """
    await is_owner(user=user, task=task, session=session)
    await crud.delete_task(session=session, task=task)