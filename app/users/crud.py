"""CRUD операции для работы с юзерами в асинхронном режиме."""

from typing import  List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from app.models import User


async def get_users(
        session: AsyncSession,
) -> List[User]:
    """
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Список пользователей.
    """
    statement = select(User).order_by(User.id)
    result: Result = await session.execute(statement)
    users = result.scalars().all()
    return list(users)
