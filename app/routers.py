from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from auth import router as auth_router
from users import router as user_router
from tasks import router as task_router


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router, dependencies=[Depends(http_bearer)])
router.include_router(task_router)

