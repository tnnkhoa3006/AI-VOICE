from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db import engine
from app.models import Base
from app.routers import health, me, projects, tts, voices

app = FastAPI(title=settings.app_name)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.cors_origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
  if settings.auto_create_tables:
    Base.metadata.create_all(bind=engine)


if settings.storage_backend == "local":
  Path(settings.local_storage_path).mkdir(parents=True, exist_ok=True)
  app.mount("/media", StaticFiles(directory=settings.local_storage_path), name="media")

app.include_router(health.router)
app.include_router(health.router, prefix="/api/v1")
app.include_router(me.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tts.router, prefix="/api/v1")
app.include_router(voices.router, prefix="/api/v1")
