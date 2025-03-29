from fastapi import APIRouter
from schemas.users import UserRead, UserUpdate
from app.auth.fastapi_users_router import fastapi_users
from .views import router as views_router


router = APIRouter(tags=["Users"])

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)

router.include_router(views_router)
