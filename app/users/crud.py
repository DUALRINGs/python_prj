from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

def create_user1(user_in: User) -> dict:
	user = user_in.model_dump()
	return {'succeess': True,
			'user': user,

	}

async def get_users(session: AsyncSession) -> list[User]:
	statement = select(User).order_by(User.id)
	result: Result = await session.execute(statement)
	users = result.scalars.all()
	return list(users)


async def get_user(session: AsyncSession, user_id: int) -> User | None:
	return await session.get(User, user_id)

async def create_user(session: AsyncSession, user_in: User) -> User:
	user = User(**user_in.model_dump())
	session.add(user)
	await session.commit()
	await session.refresh(user)
	return user


def delete_user(user_in: User) -> dict:
	user = user_in.model_dump()