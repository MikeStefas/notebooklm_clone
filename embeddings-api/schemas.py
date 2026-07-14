import uuid
from pydantic import BaseModel

class EmbedFileDTO(BaseModel):
    project_id: uuid.UUID
    file_id: uuid.UUID
    file_name: str

class DeleteEmbeddingsDTO(BaseModel):
    project_id: uuid.UUID
    file_id: uuid.UUID

class SearchDTO(BaseModel):
    prompt: str
    project_id: uuid.UUID
    file_id: uuid.UUID
