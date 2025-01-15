from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users import crud
from models import helper
from .schemas import User, UserResponse
from . import crud


router = APIRouter(prefix='/users', tags=['Users'])




@router.get("/", response_model=User)
async def get_users(
	session: AsyncSession = Depends(helper.session_dependency),
):
	return await crud.get_users(session=session)



@router.get("/{user_id}", response_model=UserResponse)
async def user_by_id(
    user_id: int,
    session: AsyncSession = Depends(helper.scoped_session_dependency),
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


@router.post("/",  response_model=User)
async def create_user(
	user_in: User,
	session: AsyncSession = Depends(helper.session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)

@router.put("/{user_id}")
def update_user_info():
	pass

@router.delete("/{user_id}")
def delete_user():
	pass