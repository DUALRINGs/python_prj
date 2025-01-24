from fastapi import FastAPI
import uvicorn
from users.views import router as users_router
from tasks.views import router as tasks_router
from auth.views import router as auth_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(auth_router)



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)