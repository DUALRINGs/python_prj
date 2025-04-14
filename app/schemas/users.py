"""Pydantic схемы пользователя для операций CRUD с валидацией имени."""

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import Len


class BaseUser(BaseModel):
    """Базовые поля пользователя с валидацией имени (4-20 символов)."""
    name: Annotated[str, Len(4, 20)]

class UserRead(schemas.BaseUser[int], BaseUser):
    """Схема для чтения пользователя (все поля)."""
    pass

class UserCreate(schemas.BaseUserCreate, BaseUser):
    """Схема регистрации с email, password и name."""
    pass

class UserUpdate(schemas.BaseUserUpdate, BaseUser):
    """Схема обновления (все поля optional)."""
    pass
