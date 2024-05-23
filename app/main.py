import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1.task_endpoint import router as task_router
from dependencies import get_task_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    task_manager = get_task_manager()
    await task_manager.init_queue()
    yield
    await task_manager.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(task_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7878)
