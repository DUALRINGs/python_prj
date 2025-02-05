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
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    task: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)