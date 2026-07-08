from sqlmodel import SQLModel
from datetime import datetime
import uuid
from typing import Optional, List

class PostProjectDTO(SQLModel):
    title : str

class PostFileToProjectDTO(SQLModel):
    title: str


class ProjectByIdResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime
    file_count: int
