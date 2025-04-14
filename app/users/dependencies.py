"""Функции зависимостей для проверки прав пользователей (суперпользователь)."""

from fastapi import Depends, HTTPException, status
from app.models import User
from auth.fastapi_users_router import current_user


async def is_superuser(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
