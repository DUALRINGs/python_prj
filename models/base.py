from sqlalchemy.orm import DeclaratevBase, Mapped, mapped_column, declared_attr


class Base(DeclaratevBase):
	__abstract__ = True

	@declared_attr.directive
	def __tablename__(cls) -> str:
		return f"{cls.__name__.lower}"

	id: Mapped[int] = mapped_column(primary_key=True)