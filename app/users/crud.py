from models import User, Task
from .schemas import UserUpdatePartial
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from auth.utils import hash_password

async def create_user(session: AsyncSession, user_in: User) -> User:
	user = User(**user_in.model_dump())
	user.password = hash_password(user.password)
	session.add(user)
	await session.commit()
	return user

async def get_users(session: AsyncSession) -> list[User]:
	statement = select(User).order_by(User.id)
	result: Result = await session.execute(statement)
	users = result.scalars().all()
	return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
	return await session.get(User, user_id)

async def update_user(
	session: AsyncSession,
	user: User,
	user_update: User | UserUpdatePartial,
	partial: bool = False,
) -> User:
	for name, value in user_update.model_dump(exclude_unset=partial).items():
		setattr(user, name, value)
	await session.commit()
	return user


async def delete_user(
	session: AsyncSession,
	user: User,
) -> None:
	await session.delete(user)
	await session.commit()