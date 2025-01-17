from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from users import crud
from models import helper
from .schemas import User, UserResponse, UserUpdatePartial
from . import crud
from .dependencies import user_by_id


router = APIRouter(prefix='/users', tags=['Users'])




@router.get("/", response_model=list[UserResponse])
async def get_users(
	session: AsyncSession = Depends(helper.session_dependency),
):
	return await crud.get_users(session=session)



@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    user: User = Depends(user_by_id),
):
    return user


@router.post("/",  response_model=User)
async def create_user(
	user_in: User,
	session: AsyncSession = Depends(helper.session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)

@router.put("/{user_id}")
async def update_user(
    user_update: User,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> User:
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )

@router.patch("/{user_id}/")
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(helper.scoped_session_dependency),
):
    return await crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
        partial=True,
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> None:
    await crud.delete_user(session=session, user=user)