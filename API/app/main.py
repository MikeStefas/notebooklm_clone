import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import create_db_and_tables
from app.features.auth.router import router as auth_router
from app.features.projects.router import router as projects_router
from app.features.files.router import router as files_router
from app.features.messages.router import router as messages_router

from app.core.minio_client import create_bucket

MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "file_storage")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_bucket(MINIO_BUCKET_NAME)
    yield




from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(files_router)
app.include_router(messages_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}