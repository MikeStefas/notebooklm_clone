from sqlmodel import SQLModel
from datetime import datetime
import uuid
from typing import Optional, List
from app.core.db import File as FileModel

class PostProjectDTO(SQLModel):
    title: str
    filename: Optional[str] = None
    content_type: Optional[str] = None

class PostFileToProjectDTO(SQLModel):
    title: str


class GetAllProjectsResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    file: Optional[FileModel] = None


class GetProjectByIdResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    file: Optional[FileModel] = None

class GetProjectResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    file: Optional[FileModel] = None

class PostProjectResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    file: Optional[FileModel] = None
    upload_url: Optional[str] = None
    fields: Optional[dict] = None


