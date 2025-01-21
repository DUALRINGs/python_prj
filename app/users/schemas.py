from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Annotated, Optional
from annotated_types import Len
from models.task import TaskStatus

# Модель для создания пользователя (без id)
class User(BaseModel):
    name: Annotated[str, Len(4, 20)]
    email: EmailStr
    password: str

# Модель для ответа (с id)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserUpdatePartial(User):
    name: Annotated[str, Len(4, 20)] | None = None
    email: EmailStr | None = None
    password: str | None = None