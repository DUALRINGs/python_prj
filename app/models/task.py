from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from .user import User


class TaskStatus(PyEnum):
    """Перечисление статусов задачи.

    Attributes:
        NEW: Задача только создана и не начата
        IN_PROGRESS: Задача в процессе выполнения
        COMPLETED: Задача успешно завершена
    """
    NEW = "новая"
    IN_PROGRESS = "в процессе"
    COMPLETED = "завершена"


class Task(Base):
    """Модель задачи в системе.

    Содержит информацию о задаче, ее статусе и связанном пользователе.
    Соответствует таблице 'tasks' в базе данных.

    Attributes:
        id: Уникальный идентификатор задачи
        title: Заголовок задачи
        description: Подробное описание задачи
        status: Текущий статус задачи (из перечисления TaskStatus)
        user_id: ID связанного пользователя (внешний ключ)
        user: Связь с моделью пользователя (relationship)
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="task")
