"""Главный роутер приложения, объединяющий все модульные роутеры (аутентификация, пользователи, задачи)."""

from fastapi import APIRouter
from auth.fastapi_users_router import router as auth_router
from users import router as user_router
from tasks import router as task_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(task_router)
