from typing import TYPE_CHEKING
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from enum import Enum as PyEnum

if TYPE_CHEKING:
	from .user import User

class TaskStatus(PyEnum):
    NEW = "новая"
    IN_PROGRESS = "в процессе"
    COMPLETED = "завершена"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")