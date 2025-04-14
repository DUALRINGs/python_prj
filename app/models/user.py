"""Модель пользователя с аутентификацией FastAPI Users и связью с задачами."""

from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from .base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

if TYPE_CHECKING:
    from .task import Task
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, SQLAlchemyBaseUserTable[int]):
    """Модель пользователя с поддержкой аутентификации FastAPI Users.

    Включает все стандартные поля для аутентификации (email, hashed_password и т.д.)
    из SQLAlchemyBaseUserTable плюс дополнительные кастомные поля.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    task: Mapped[list["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"  # Автоматическое удаление связанных задач
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        """Создает UserDatabase для интеграции с FastAPI Users."""
        return SQLAlchemyUserDatabase(session, User)
