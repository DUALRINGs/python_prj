"""Провайдер UserManager с зависимостью от БД пользователей для FastAPI Users."""

from fastapi import Depends
from app.auth.user_manager import UserManager
from .users import get_users_db


async def get_user_manager(user_db=Depends(get_users_db)):
    """Возвращает экземпляр UserManager с инжектированной БД."""
    yield UserManager(user_db)
