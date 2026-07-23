import os
import uuid
from typing import List, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from actions import get_chunks_from_s3_file
from schemas import EmbedFileDTO, DeleteEmbeddingsDTO, SearchDTO
from background_task import embed_file_task

load_dotenv()

CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH", "./chroma_data")

async def verify_internal_secret(secret_key: str = Header(default=None)):
    expected_secret = os.getenv("INTERNAL_API_SECRET")
    if not secret_key or secret_key != expected_secret:
        raise HTTPException(status_code=403, detail="Unauthorized internal request")
    return secret_key

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"msg": "Hello"}

@app.post("/embed", dependencies=[Depends(verify_internal_secret)])
async def create_embeddings(payload: EmbedFileDTO, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(embed_file_task, payload, request.app.state.chroma_client)
    
    return {
        "status": "processing"
    }

@app.post("/delete", dependencies=[Depends(verify_internal_secret)])
async def delete_embeddings(payload: DeleteEmbeddingsDTO, request: Request):
    chroma_client = request.app.state.chroma_client
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

@app.post("/search", dependencies=[Depends(verify_internal_secret)])
async def query_embeddings(payload: SearchDTO, request: Request):
    chroma_client = request.app.state.chroma_client
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
    