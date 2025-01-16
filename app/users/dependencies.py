from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import helper, User

from . import crud


async def user_by_id(
    user_id: int,
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )