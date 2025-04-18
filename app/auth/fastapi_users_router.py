"""Роутер FastAPI для аутентификации и регистрации пользователей с использованием FastAPIUsers."""

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from dependencies.authentication.backend import auth_backend
from app.models import User
from dependencies.authentication.user_manager import get_user_manager
from schemas.users import UserRead, UserCreate


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter(tags=["Auth"])

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth"
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth"
)
