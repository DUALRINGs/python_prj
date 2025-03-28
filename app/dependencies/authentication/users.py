from typing import (TYPE_CHECKING, Annotated)
from fastapi import Depends
from app.models import (db_helper, User)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(session: Annotated["AsyncSession", Depends(db_helper.session_getter)]):
    """Возвращает объект доступа к БД пользователей для заданной сессии."""
    yield User.get_db(session=session)
