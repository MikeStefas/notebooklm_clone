from sqlmodel import SQLModel
from datetime import datetime
import uuid
from app.core.db import SenderType

class PostUserMessageDTO(SQLModel):
    content: str

class MessageResponse(SQLModel):
    id: uuid.UUID
    project_id: uuid.UUID
    content: str
    sender: SenderType
    created_at: datetime
