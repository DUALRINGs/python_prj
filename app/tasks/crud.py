from models import User, Task
from .schemas import TaskUpdatePartial, TaskResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from auth.dependencies import get_current_auth_user

from fastapi import Depends

async def create_task(
	user: User,
	task_in: Task,
	session: AsyncSession,
	) -> Task:
	task = Task(**task_in.model_dump())
	task.user = user
	session.add(task)
	await session.commit()
	return task

async def get_tasks(session: AsyncSession, user: User) -> list[Task]:
	statement = select(Task).where(Task.user_id == user.id)
	result: Result = await session.execute(statement)
	tasks = result.scalars().all()
	return list(tasks)


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
	return await session.get(Task, task_id)

async def update_task(
	user: User,
	session: AsyncSession,
	task: Task,
	task_update: Task | TaskUpdatePartial,
	partial: bool = False,
) -> Task:
	for name, value in task_update.model_dump(exclude_unset=partial).items():
		setattr(task, name, value)  
	await session.commit()
	return task



async def delete_task(
	session: AsyncSession,
	task: Task, 
) -> None:
	await session.delete(task)
	await session.commit()