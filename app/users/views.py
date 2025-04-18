"""Роутер для административных операций с пользователями (только для суперпользователей)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
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
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список пользователей.
    """
    return await get_users(session=session)
