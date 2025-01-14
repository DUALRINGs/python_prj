from fastapi import APIRouter
from users import crud
from users.schemas import User


router = APIRouter(prefix='/users', tags=['Users'])




@router.get("/")
def get_users_list():
	return {'massenge': None}

@router.get("/{user_id}")
def get_user_by_id(user_id: int):
	return {'user_id': user_id}

@router.post("/")
def create_user(user: User):
    return crud.create_user(user_in=user)

@router.put("/{user_id}")
def update_user_info():
	pass

@router.delete("/{user_id}")
def delete_user():
	pass