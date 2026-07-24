import os
import httpx
from loguru import logger
from dotenv import load_dotenv
from actions import get_chunks_from_s3_file
from schemas import EmbedFileDTO
from dependencies import get_chroma_collection
import math
load_dotenv()


def embed_file_task(payload: EmbedFileDTO, chroma_client):
    backend_url = os.getenv("BACKEND_URL")
    secret = os.getenv("INTERNAL_API_SECRET")
    headers = {"secret": secret}

    try:
        key = f"{payload.project_id}/{payload.file_id}/{payload.file_name}"
        logger.info(f"Starting embedding task for key: {key}")
        chunks = get_chunks_from_s3_file(key)
        logger.info(f"Retrieved {len(chunks)} chunks")

        if not chunks:
            logger.warning(f"No chunks found for key: {key}")
            httpx.post(f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/fail-process", headers=headers)
            return

        try:
            collection = get_chroma_collection(chroma_client, str(payload.project_id), task_type="RETRIEVAL_DOCUMENT")
        except Exception as e:
            logger.error(f"Failed to get/create collection for project {payload.project_id}: {e}")
            httpx.post(f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/fail-process", headers=headers)
            return


        request_count = math.ceil(len(chunks) / 100)
        for i in range(request_count):
            batch = chunks[i*100:i*100 + 100]
            ids = [f"{payload.file_id}-{j}" for j in range(len(batch))]
            metadata = [
                {
                    "file_id": str(payload.file_id),

                    "project_id": str(payload.project_id),
                    "chunk_index": j + (i * 100),
                }
                for j in range(len(batch))
            ]
            
            collection.add(
                documents=batch,
                ids=ids,
                metadatas=metadata
            )
            
            
        logger.info(f"Successfully added {len(chunks)} embeddings to Chroma for file {payload.file_id}")

        url = f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/confirm-process"
        r = httpx.post(url, headers=headers)
        logger.info(f"Confirm-process response: {r.status_code}")

    except Exception as e:
        logger.exception(f"Unhandled exception in embed_file_task for file {payload.file_id}: {e}")
        try:
            httpx.post(f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/fail-process", headers=headers)
        except Exception as callback_err:
            logger.error(f"Failed to send failure callback: {callback_err}")