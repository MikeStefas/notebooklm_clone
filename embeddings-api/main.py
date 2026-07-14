import os
import uuid
from typing import List, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from actions import get_chunks_from_s3_file
from schemas import EmbedFileDTO, DeleteEmbeddingsDTO, SearchDTO
from background_task import embed_file_task

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

@app.post("/embed")
async def create_embeddings(payload: EmbedFileDTO, background_tasks: BackgroundTasks):
    background_tasks.add_task(embed_file_task, payload)
    
    return {
        "status": "processing"
    }

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
    