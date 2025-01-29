from http.client import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import crud
from app.models import helper
from .schemas import User, UserResponse, UserUpdatePartial
from .dependencies import user_by_id, is_admin_or_owner
from app.auth.dependencies import get_current_auth_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(
    session: AsyncSession = Depends(helper.session_dependency),
) -> list[User]:
    """
    Возвращает список всех пользователей.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список пользователей.
    """
    return await crud.get_users(session=session)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user: User = Depends(user_by_id),
) -> User:
    """
    Возвращает пользователя по его идентификатору.

    :param user: Пользователь, найденный по идентификатору.
    :return: Пользователь.
    """
    return user



@router.post("/", response_model=User)
async def create_user(
    user_in: User,
    session: AsyncSession = Depends(helper.session_dependency),
) -> User:
    """
    Создает нового пользователя.

    :param user_in: Данные для создания пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Созданный пользователь.
    """
    # Попытка создать пользователя
    user = await crud.create_user(session=session, user_in=user_in)
    return user


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: User,
    user: User = Depends(get_current_auth_user),
    user_to_update: User = Depends(user_by_id),
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> User:
    """
    Полностью обновляет данные пользователя.

    :param user_id: Идентификатор пользователя, которого нужно обновить.
    :param user_update: Данные для обновления.
    :param user: Текущий аутентифицированный пользователь.
    :param user_to_update: Пользователь, которого нужно обновить.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Обновленный пользователь.
    """
    await is_admin_or_owner(user=user, user_id=user_id, session=session)
    return await crud.update_user(
        session=session,
        user=user_to_update,
        user_update=user_update,
    )


@router.patch("/{user_id}/")
async def update_user_partial(
    user_id: int,
    user_update: UserUpdatePartial,
    user: User = Depends(get_current_auth_user),
    user_to_update: User = Depends(user_by_id),
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> User:
    """
    Частично обновляет данные пользователя.

    :param user_id: Идентификатор пользователя, которого нужно обновить.
    :param user_update: Данные для обновления.
    :param user: Текущий аутентифицированный пользователь.
    :param user_to_update: Пользователь, которого нужно обновить.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Обновленный пользователь.
    """
    await is_admin_or_owner(user=user, user_id=user_id, session=session)
    return await crud.update_user(
        session=session,
        user=user_to_update,
        user_update=user_update,
        partial=True,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user: User = Depends(get_current_auth_user),
    user_to_delete: User = Depends(user_by_id),
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> None:
    """
    Удаляет пользователя.

    :param user_id: Идентификатор пользователя, которого нужно удалить.
    :param user: Текущий аутентифицированный пользователь.
    :param user_to_delete: Пользователь, которого нужно удалить.
    :param session: Асинхронная сессия SQLAlchemy.
    """
    await is_admin_or_owner(user=user, user_id=user_id, session=session)
    await crud.delete_user(session=session, user=user_to_delete)