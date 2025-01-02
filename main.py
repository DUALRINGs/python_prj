from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/users")
def get_users_list():
	return {'massenge': None}

@app.get("/users/{user_id}")
def get_user_id(user_id: int):
	return {'user_id': user_id}

@app.post("/users")
def create_user():
	pass

@app.put("/users/{user_id}")
def update_user_info():
	pass

@app.delete("/users/{user_id}")
def delete_user():
	pass

@app.get('/tasks')
def get_tasks():
	pass

@app.get('/tasks/{task_id}')
def get_task():
	pass

@app.post('/tasks')
def post_task():
	pass

@app.put('tasks/{task_id}')
def update_task():
	pass

@app.delete('/tasks/{task_id}')
def delete_task():
	pass



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)