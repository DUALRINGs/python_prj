import uuid

from fastapi_users import FastAPIUsers

from dependencies.authentication.backend import auth_backend
from app.models import User
from dependencies.authentication.user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

