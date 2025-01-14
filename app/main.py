from fastapi import FastAPI
import uvicorn
from models import Base, helper
from models.user import User
from users.views import router as users_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)