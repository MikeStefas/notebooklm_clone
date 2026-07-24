from pathlib import Path
import requests
import httpx
import uuid
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi import HTTPException

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

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env", override=True)
load_dotenv(override=True)

def get_config():
    api_url = os.getenv("EMBEDDINGS_API_URL", "http://localhost:8001")
    secret = os.getenv("INTERNAL_API_SECRET", "your_secret_password") or ""
    return api_url, secret

async def request_embed(payload: EmbedFileDTO):
    api_url, secret = get_config()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{api_url}/embed", json=payload.model_dump(mode="json"), headers={"secret": secret})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="External embeddings api request failed")
        return response.json()

async def request_delete(payload: DeleteEmbeddingsDTO):
    api_url, secret = get_config()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{api_url}/delete", json=payload.model_dump(mode="json"), headers={"secret": secret})
        if response.status_code not in (200, 404):
            raise HTTPException(status_code=response.status_code, detail="External embeddings api request failed")
        return response.json() if response.status_code == 200 else {"status": "not_found"}

async def request_search(payload: SearchDTO):
    api_url, secret = get_config()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{api_url}/search", json=payload.model_dump(mode="json"), headers={"secret": secret})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="External embeddings api request failed")
        return response.json()