from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=['Tasks'])


@router.get('/')
def get_tasks_list():
	pass

@router.get('/{task_id}')
def get_task_by_id(task_id: int):
	return {'task_id': task_id}

@router.post('/')
def post_task():
	pass

@router.put('/{task_id}')
def update_task():
	pass

@router.delete('/{task_id}')
def delete_task():
	pass