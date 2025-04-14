"""Менеджер пользователей FastAPI с обработкой событий регистрации и базовой аутентификации."""

import logging
from typing import Optional, TYPE_CHECKING
from app.models import User
from fastapi_users import (BaseUserManager, IntegerIDMixin)


if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей с целочисленными ID.

    Обеспечивает базовую логику управления пользователями:
    - Регистрация
    - Аутентификация
    - Обработка событий (например, post-registration)

    Наследуется:
    - IntegerIDMixin: Поддержка целочисленных идентификаторов.
    - BaseUserManager: Базовый функционал менеджера пользователей.
    """
    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ) -> None:
        """Вызывается после успешной регистрации пользователя."""
        log.warning("User %r has registered.", user.id)
