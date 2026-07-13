from sqlmodel import SQLModel
from datetime import datetime
import uuid

class FileResponse(SQLModel):
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    nextcloud_path: str
    created_at: datetime
    updated_at: datetime

class PresignedUrlResponse(SQLModel):
    url: str

class FilePresignedUploadResponse(SQLModel):
    file_created: FileResponse
    url: str
    fields: dict[str, str]

