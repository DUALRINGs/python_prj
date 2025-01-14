from .base import Base
from sqlalchemy.orm import Mapped
from pydantic import EmailStr
from typing import Annotated
from annotated_types import Len


class User(Base):
	__tablename__ = "users"
	
	name: Mapped[str]
	email: Mapped[str]
	password: Mapped[str]