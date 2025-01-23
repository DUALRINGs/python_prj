from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import User
from models import helper, Task
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result


from . import crud


async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> Task:
    task = await crud.get_task(session=session, task_id=task_id)
    if task:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )
    
async def is_owner(
    user: User,
    task: Task,
    session: AsyncSession = Depends(helper.scoped_session_dependency),
    ):
    result: Result = await session.execute(
        select(Task)
        .options(selectinload(Task.user))  # Загружаем связанного пользователя
    )
    if user.id is not task.user.id:  # Предполагаем, что user_id — это поле в Task
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the owner of this task!",
        )
