from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.schemas import User
from dependencies.authentication.backend import authentication_backend
from schemas.users import UserRead, UserCreate
from . import utils
from .dependencies import (
    validate_auth_user,
    get_current_token_payload,
    get_current_auth_user,
)
from .schemas import TokenInfo
from .fastapi_users_router import fastapi_users

router = APIRouter(prefix="/auth")
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_auth_router(authentication_backend),
)
'''
@router.post("/login")
async def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
) -> TokenInfo:
    """
    Генерирует JWT-токен для аутентифицированного пользователя.

    :param user: Аутентифицированный пользователь.
    :return: Объект TokenInfo с access_token.
    """
    jwt_payload = {
        "sub": user.email,
        "username": user.name,
        "email": user.email,
    }
    token = await utils.encode_jwt(jwt_payload)

    return TokenInfo(access_token=token)
'''

@router.get("/users/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
) -> dict:
    """
    Возвращает информацию о текущем аутентифицированном пользователе.

    :param payload: Payload JWT-токена.
    :param user: Текущий аутентифицированный пользователь.
    :return: Словарь с информацией о пользователе.
    """
    iat = payload.get("iat")
    return {
        "user_id": user.id,
        "username": user.name,
        "email": user.email,
        "logged_in_at": iat,
    }