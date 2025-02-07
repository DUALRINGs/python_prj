from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.fastapi_users_router import current_user

from models import db_helper, User
from schemas.users import UserRead
from users.crud import get_users
from users.dependencies import is_superuser

router = APIRouter(prefix='/users', dependencies=[Depends(is_superuser)])


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> list[User]:
    """
    Возвращает список пользователей.

    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список пользователей.
    """
    return await get_users(session=session)