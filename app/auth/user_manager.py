import logging
from typing import Optional, TYPE_CHECKING
from app.models import User
from fastapi_users import (BaseUserManager, IntegerIDMixin)

if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )
