from pydantic import BaseModel, EmailStr
from typing import Annotated 
from annotated_types import MinLen, MaxLen


class User(BaseModel):
	id: int
	name: Annotated[str, MinLen(3), MaxLen(15)]
	email: EmailStr
	password: str