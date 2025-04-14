"""Pydantic схемы задач"""


from pydantic import BaseModel
from typing import Annotated
from annotated_types import Len
from app.models.task import TaskStatus


class Task(BaseModel):
    """Основная модель задачи с обязательными полями и валидацией."""
    id: int
    title: Annotated[str, Len(4, 40)]
    description: str
    status: TaskStatus

class TaskResponse(Task):
    """Модель для ответов API (наследует все поля Task)."""
    pass

class TaskUpdatePartial(Task):
    title: Annotated[str, Len(4, 40)] | None = None
    description: str | None = None
    status: TaskStatus | None = None
