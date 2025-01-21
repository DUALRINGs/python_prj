from models import User, Task
from .schemas import UserUpdatePartial
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result


async def create_task(session: AsyncSession, task_in: Task,) -> Task:
	task = Task(**task_in.model_dump())
	session.add(task)
	await session.commit()
	return task

async def get_tasks(session: AsyncSession) -> list[Task]:
	statement = select(Task).order_by(Task.id)
	result: Result = await session.execute(statement)
	tasks = result.scalars().all()
	return list(tasks)


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
	return await session.get(Task, task_id)

async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: Task | UserUpdatePartial,
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