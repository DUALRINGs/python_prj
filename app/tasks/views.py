from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from tasks import crud
from models import helper
from .schemas import Task, TaskUpdatePartial, TaskResponse
from . import crud
from auth.dependencies import get_current_auth_user
from users.schemas import User
from .dependencies import task_by_id
from .dependencies import is_owner

router = APIRouter(prefix='/task', tags=['Tasks'])


@router.get("/", response_model=list[Task])
async def get_tasks(
	user: User = Depends(get_current_auth_user),
	session: AsyncSession = Depends(helper.session_dependency),
):
	return await crud.get_tasks(session=session, user=user)

@router.get("/{task_id}", response_model=Task)
async def get_task_by_id(
	task_id: int,
	task: Task = Depends(task_by_id),
):
	return task



@router.post("/",  response_model=Task)
async def create_task(
	task_in: Task,
	user: User = Depends(get_current_auth_user),
	session: AsyncSession = Depends(helper.session_dependency),
):
	return await crud.create_task(user=user, session=session, task_in=task_in)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
	task_update: TaskUpdatePartial,
	user: User = Depends(get_current_auth_user),
	task: Task = Depends(task_by_id),
	session: AsyncSession = Depends(helper.scoped_session_dependency),
):
	await is_owner(user=user, task=task, session=session)
	updated_task = await crud.update_task(
		user=user,
		session=session,
		task=task,
		task_update=task_update,
	)
	return updated_task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
	task_update: TaskUpdatePartial,
	user: User = Depends(get_current_auth_user),
	task: Task = Depends(task_by_id),
	session: AsyncSession = Depends(helper.scoped_session_dependency),
):
	await is_owner(user=user, task=task, session=session)
	updated_task = await crud.update_task(
		user=user,
		session=session,
		task=task,
		task_update=task_update,
		partial=True,
	)
	return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
	user: User = Depends(get_current_auth_user),
	task: Task = Depends(task_by_id),
	session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> None:
	await is_owner(user=user, task=task, session=session)
	await crud.delete_task(session=session, task=task)