import os
import uuid
from typing import List, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from dotenv import load_dotenv
from loguru import logger
from actions import get_chunks_from_s3_file
from schemas import EmbedFileDTO, DeleteEmbeddingsDTO, SearchDTO
from background_task import embed_file_task

load_dotenv()

CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH", "./chroma_data")

async def verify_internal_secret(secret: str = Header(default=None, alias="secret")):
    expected_secret = os.getenv("INTERNAL_API_SECRET")
    if not secret or secret != expected_secret:
        logger.warning("Unauthorized internal request attempt")
        raise HTTPException(status_code=403, detail="Unauthorized internal request")
    return secret

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Initializing ChromaDB PersistentClient at path: {CHROMA_DATA_PATH}")
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
    logger.info("Root endpoint health check accessed")
    return {"msg": "Hello"}

@app.post("/embed", dependencies=[Depends(verify_internal_secret)])
async def create_embeddings(payload: EmbedFileDTO, request: Request, background_tasks: BackgroundTasks):
    logger.info(f"Received embed request for file {payload.file_id} ('{payload.file_name}') in project {payload.project_id}")
    background_tasks.add_task(embed_file_task, payload, request.app.state.chroma_client)
    logger.info(f"Dispatched background task embed_file_task for file {payload.file_id}")
    
    return {
        "status": "processing"
    }

@app.post("/delete", dependencies=[Depends(verify_internal_secret)])
async def delete_embeddings(payload: DeleteEmbeddingsDTO, request: Request):
    logger.info(f"Received delete embeddings request for file {payload.file_id} in project {payload.project_id}")
    chroma_client = request.app.state.chroma_client
    try:
        collection = chroma_client.get_collection(str(payload.project_id))
    except Exception as e:
        logger.error(f"Collection for project {payload.project_id} not found: {e}")
        raise HTTPException(status_code=404, detail="Collection not found")
    
    collection.delete(
        where={
            "file_id": str(payload.file_id)
        }
    )
    logger.info(f"Successfully deleted embeddings for file {payload.file_id} in project {payload.project_id}")
    
    return {
        "status": "success"
    }

@app.post("/search", dependencies=[Depends(verify_internal_secret)])
async def query_embeddings(payload: SearchDTO, request: Request):
    logger.info(f"Received search request for file {payload.file_id} in project {payload.project_id} with prompt: '{payload.prompt}'")
    chroma_client = request.app.state.chroma_client
    try:
        collection = chroma_client.get_collection(str(payload.project_id))
    except Exception as e:
        logger.error(f"Collection for project {payload.project_id} not found: {e}")
        raise HTTPException(status_code=404, detail="Collection not found")
    
    results = collection.query(
        query_texts=[payload.prompt],
        n_results=5,
        where={"file_id": str(payload.file_id)}
    )
    if not results["ids"] or len(results["ids"][0]) == 0:
        logger.warning(f"No embeddings found for file {payload.file_id} in project {payload.project_id}")
        raise HTTPException(status_code=404, detail="No embeddings found")

    logger.info(f"Successfully retrieved {len(results['documents'][0])} document chunk(s) for file {payload.file_id}")
    return results["documents"][0]
    