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
from .schemas import TokenInfo

router = APIRouter()

@router.post("/login")
async def auth_user_issue_jwt(
	user: User = Depends(validate_auth_user),
):
	jwt_payload = {
		"sub": user.email,
		"username": user.name,
		"email": user.email,
	}
	token = await utils.encode_jwt(jwt_payload)
	#return RedirectResponse(url="/users", status_code=status.HTTP_303_SEE_OTHER)
	return TokenInfo(
		access_token=token,
	)



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