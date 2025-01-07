from fastapi import FastAPI
import uvicorn
from task_views import router as task_router
from users.views import router as users_router

app = FastAPI()
app.include_router(task_router)
app.include_router(users_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)