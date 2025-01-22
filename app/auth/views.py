from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from users import crud
from models import helper
from users.schemas import User, UserResponse, UserUpdatePartial, User
from . import utils
from fastapi.responses import RedirectResponse
from .dependencies import *
from fastapi.security import OAuth2PasswordBearer
from authlib.jose import JsonWebToken, errors

router = APIRouter(prefix="/login")


# Схема OAuth2 для извлечения токена из заголовка Authorization
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_token_payload(
    token: str = Depends(oauth2_schema),
) -> dict:
    token = credentials.credentials 

    try:
        # Декодируем токен (если decode_jwt асинхронная, добавьте await)
        payload = await utils.decode_jwt(token=token)
    except errors.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
    except errors.ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except errors.BadSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
        )
    except errors.InvalidClaimError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token claims: {e}",
        )
    except errors.MissingClaimError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing required claims: {e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {e}",
        )
    return payload

async def get_current_auth_user(
    session: AsyncSession = Depends(helper.session_dependency),
    payload: dict = Depends(get_current_token_payload),
) -> User:

    email: str | None = payload.get("email")
    if user := await user_by_email(session=session, email=email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
@router.post("/")
async def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.name,
        "username": user.name,
        "email": user.email,
    }
    token = await utils.encode_jwt(jwt_payload)
   #return RedirectResponse(url="/users", status_code=status.HTTP_303_SEE_OTHER)
    return {'token': token}


@router.get("/users/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.name,
        "email": user.email,
        "logged_in_at": iat,
    }

