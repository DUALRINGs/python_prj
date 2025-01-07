from .base import Base
from sqlalchemy.orm import Mapped
from pydantic import EmailStr


class User(Base):
	name: Mapped[Annotated[str, MinLen(3), MaxLen(15)]]
	email: Mapped[EmailStr]
	password: Mapped[str]