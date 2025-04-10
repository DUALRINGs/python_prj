from pydantic import BaseModel
from typing import Annotated, Optional
from annotated_types import Len
from app.models.task import TaskStatus


class Task(BaseModel):
    """Основная модель задачи с обязательными полями и валидацией."""
    title: Annotated[str, Len(4, 40)]
    description: str
    status: TaskStatus

class TaskResponse(Task):
    """Модель для ответов API (наследует все поля Task)."""
    pass

class TaskUpdatePartial(Task):
    """Модель для частичного обновления (поддержка PATCH)."""
    title: Annotated[str, Len(4, 40)] | None = None
    description: str | None = None
    status: TaskStatus | None = None
