import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from loguru import logger
from schemas import EmbedFileDTO, DeleteEmbeddingsDTO, SearchDTO
from background_task import embed_file_task
from dependencies import create_chroma_client, get_chroma_collection

load_dotenv()


async def verify_internal_secret(secret: str = Header(default=None, alias="secret")):
    expected_secret = os.getenv("INTERNAL_API_SECRET")
    if not secret or secret != expected_secret:
        logger.warning("Unauthorized internal request attempt")
        raise HTTPException(status_code=403, detail="Unauthorized internal request")
    return secret


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ChromaDB PersistentClient via FastAPI lifespan...")
    app.state.chroma_client = create_chroma_client()
    yield
    logger.info("FastAPI lifespan shutdown...")


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
    return {"status": "processing"}


@app.post("/delete", dependencies=[Depends(verify_internal_secret)])
async def delete_embeddings(payload: DeleteEmbeddingsDTO, request: Request):
    logger.info(f"Received delete embeddings request for file {payload.file_id} in project {payload.project_id}")
    collection = get_chroma_collection(request.app.state.chroma_client, str(payload.project_id))
    collection.delete(where={"file_id": str(payload.file_id)})
    logger.info(f"Successfully deleted embeddings for file {payload.file_id} in project {payload.project_id}")
    return {"status": "success"}


@app.post("/search", dependencies=[Depends(verify_internal_secret)])
async def query_embeddings(payload: SearchDTO, request: Request):
    logger.info(f"Received search request  in project {payload.project_id} with prompt: '{payload.prompt}'")
    collection = get_chroma_collection(request.app.state.chroma_client, str(payload.project_id), task_type="RETRIEVAL_QUERY")
    results = collection.query(
        query_texts=[payload.prompt],
        n_results=5,
    )
    if not results["ids"] or len(results["ids"][0]) == 0:
        logger.warning(f"No embeddings found in project {payload.project_id}")
        raise HTTPException(status_code=404, detail="No embeddings found")

    logger.info(f"Successfully retrieved {len(results['documents'][0])} document chunk(s) ")
    return results["documents"][0]