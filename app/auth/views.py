from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import User
from dependencies.authentication.backend import auth_backend
from schemas.users import UserRead, UserCreate, UserUpdate

from .fastapi_users_router import fastapi_users



router = APIRouter(tags=["Auth"])

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth"
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth"
)
