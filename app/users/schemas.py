from pydantic import BaseModel, EmailStr
from typing import Annotated 
from annotated_types import Len


class User(BaseModel):
	id: int
	name: Annotated[str, Len(4, 20)]
	email: EmailStr
	password: str