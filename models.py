from fastapi import BaseModel
from pydantic import EmailStr
from enum import Enum

class StateEnum(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    end = 'end'


class User(BaseModel):
	id: int
	name: str
	email: EmailStr
	passwd: str


class Task(BaseModel):
	id: int
	name: str
	descrip: str
	state: StateEnum = StateEnum.new
	user_id: int