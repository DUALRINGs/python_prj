"""Базовый класс SQLAlchemy моделей с автогенерацией имён таблиц в множественном числе."""

from sqlalchemy.orm import (DeclarativeBase, declared_attr)


class Base(DeclarativeBase):
	"""Базовый класс моделей с автоматической генерацией имен таблиц."""
	__abstract__ = True

	@declared_attr.directive
	def __tablename__(cls) -> str:
		return f"{cls.__name__.lower()}s"
