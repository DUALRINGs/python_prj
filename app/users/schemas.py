from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated, Optional
from annotated_types import Len
from app.models.task import TaskStatus


class User(BaseModel):
    name: Annotated[str, Len(4, 20)]
    email: EmailStr
    password: str # должно бло быть Annotated[str, Len(8, 20)] но оно почемуто валидирует хеш а не инпут

# Модель для ответа (с id)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserCreate(User):
    pass

class UserUpdatePartial(User):
    name: Annotated[str, Len(4, 20)] | None = None
    email: EmailStr | None = None
    password: str | None = None