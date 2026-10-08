from fastapi import FastAPI

from app.api.router import router
from app.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
