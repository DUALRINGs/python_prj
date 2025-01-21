from pydantic import BaseModel
from typing import Annotated, Optional
from annotated_types import Len
from models.task import TaskStatus

class Task(BaseModel):
    title: str
    description: str
    status: TaskStatus

class TaskResponse(Task):
    pass