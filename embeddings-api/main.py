import os
import uuid
from typing import List, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from actions import get_chunks_from_s3_file
from pydantic import BaseModel
load_dotenv()

CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH", "./chroma_data")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"msg": "Hello"}

class EmbedFileDTO(BaseModel):
    key: str
    project_id: uuid.UUID
    file_id: uuid.UUID

@app.post("/embed")
async def create_embeddings(payload: EmbedFileDTO):
    chunks = get_chunks_from_s3_file(payload.key)
    
    chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    try:
        collection = chroma_client.get_or_create_collection(str(payload.project_id))
    except:
        raise HTTPException(status_code=404, detail="Collection failed to be created")
    
    if len(chunks) == 0 or not chunks:
        raise HTTPException(status_code=400, detail="No chunks found")

    for idx, chunk in enumerate(chunks):
        collection.add(
            ids=[f"{payload.key}_chunk_{idx}"],
            documents=[chunk],
            metadatas=[{
                "project_id": str(payload.project_id),
                "file_id": str(payload.file_id),
                "filename": payload.key
            }]
        )
    return {
        "status": "success",
        "chunks_processed": len(chunks)
    }

class DeleteEmbeddingsDTO(BaseModel):
    project_id: uuid.UUID
    file_id: uuid.UUID

@app.post("/delete")
async def delete_embeddings(payload: DeleteEmbeddingsDTO):
    chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    try:
        collection = chroma_client.get_collection(str(payload.project_id))
    except:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    collection.delete(
        where={
            
            "file_id": str(payload.file_id)
        }
    )
    
    return {
        "status": "success"
    }

class SearchDTO(BaseModel):
    prompt: str
    project_id: uuid.UUID
    file_id: uuid.UUID

@app.post("/search")
async def query_embeddings(payload: SearchDTO):
    chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    try:
        collection = chroma_client.get_collection(str(payload.project_id))
    except:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    results = collection.query(
        query_texts=[payload.prompt],
        n_results=2,
        where={"file_id": str(payload.file_id)}
    )
    if results["embeddings"] is None or len(results["documents"]) == 0:
        raise HTTPException(status_code=404, detail="No embeddings found")

    return {
        "results": results
    }
    