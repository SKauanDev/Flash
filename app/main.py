from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router
from app.config import settings
from app.db.init import init_db
from app.scheduler.worker import scheduler_loop


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
