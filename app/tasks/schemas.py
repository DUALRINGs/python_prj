from pydantic import BaseModel
from typing import Annotated, Optional
from annotated_types import Len
from app.models.task import TaskStatus


class Task(BaseModel):
    title: Annotated[str, Len(4, 20)]
    description: str
    status: TaskStatus

class TaskResponse(Task):
    pass

class TaskUpdatePartial(Task):
    title: Annotated[str, Len(4, 20)] | None = None
    description: str | None = None
    status: TaskStatus | None = None
