"""API роутер для CRUD операций с задачами пользователя с проверкой прав доступа."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks import crud
from app.models import db_helper
from auth.fastapi_users_router import current_user
from .schemas import Task, TaskUpdatePartial, TaskResponse
from app.models import User
from .dependencies import is_owner_or_superuser


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> list[Task]:
    """
    :param user: Текущий аутентифицированный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список задач.
    """
    return await crud.get_all_user_tasks(session=session, user=user)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Task:
    """
    :param user: Текущий аутентифицированный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :param task: Задача, найденная по идентификатору.
    :return: Задача.
    """
    task = await crud.get_task_by_id(task_id, session)
    await is_owner_or_superuser(user=user, task=task, session=session)
    return task

@router.post("/", response_model=Task)
async def create_task(
    task_in: Task,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Task:
    """
    :param task_in: Данные для создания задачи.
    :param user: Текущий аутентифицированный пользователь.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Созданная задача.
    """
    return await crud.create_task(user=user, session=session, task_in=task_in)

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_partial_endpoint(
    task_id: int,
    task_update: TaskUpdatePartial,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TaskResponse:
    """
    :param task_update: Данные для обновления задачи.
    :param user: Текущий аутентифицированный пользователь.
    :param task: Задача, которую нужно обновить.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Обновленная задача.
    """
    task = await crud.get_task_by_id(task_id, session)
    await is_owner_or_superuser(user=user, task=task, session=session)
    updated_task = await crud.update_task(
        session=session,
        task=task,
        task_update=task_update,
        partial=True,
    )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    :param user: Текущий аутентифицированный пользователь.
    :param task: Задача, которую нужно удалить.
    :param session: Асинхронная сессия SQLAlchemy.
    """
    task = await crud.get_task_by_id(task_id, session)
    await is_owner_or_superuser(user=user, task=task, session=session)
    await crud.delete_task(session=session, task=task)
