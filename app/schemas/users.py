from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import Len


class BaseUser(BaseModel):
    """Base user model with common fields."""
    name: Annotated[str, Len(4, 20)]

class UserRead(schemas.BaseUser[int], BaseUser):
    """Schema for reading user data."""
    pass

class UserCreate(schemas.BaseUserCreate, BaseUser):
    """Schema for creating a new user."""
    pass

class UserUpdate(schemas.BaseUserUpdate, BaseUser):
    """Schema for updating user data."""
    pass


class User(BaseModel):
    name: Annotated[str, Len(4, 20)]
    email: EmailStr
    password: str

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
