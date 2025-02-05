from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from models import db_helper
from routers import router



@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(router)



if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)