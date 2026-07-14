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

load_dotenv()

async def request_embed(payload: EmbedFileDTO):
    api_url = os.getenv("EMBEDDINGS_API_URL")
    secret = os.getenv("INTERNAL_API_SECRET")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{api_url}/embed", json=payload.model_dump(mode="json"), headers={"secret_key": secret})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="External embeddings api request failed")
        return response.json()

async def request_delete(payload: DeleteEmbeddingsDTO):
    api_url = os.getenv("EMBEDDINGS_API_URL")
    secret = os.getenv("INTERNAL_API_SECRET")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{api_url}/delete", json=payload.model_dump(mode="json"), headers={"secret_key": secret})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="External embeddings api request failed")
        return response.json()

async def request_search(payload: SearchDTO):
    api_url = os.getenv("EMBEDDINGS_API_URL")
    secret = os.getenv("INTERNAL_API_SECRET")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{api_url}/search", json=payload.model_dump(mode="json"), headers={"secret_key": secret})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="External embeddings api request failed")
        return response.json()