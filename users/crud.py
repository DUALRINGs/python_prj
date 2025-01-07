from users.schemas import User

def create_user(user_in: User) -> dict:
	user = user_in.model_dump()
	return {'succeess': True,
			'user': user,

	}