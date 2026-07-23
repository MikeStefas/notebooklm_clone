import os
import httpx
import chromadb
from fastapi import HTTPException
from dotenv import load_dotenv
from actions import get_chunks_from_s3_file
from schemas import EmbedFileDTO

load_dotenv()

CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH", "./chroma_data")

def embed_file_task(payload: EmbedFileDTO, chroma_client):
    backend_url = os.getenv("BACKEND_URL")
    secret = os.getenv("INTERNAL_API_SECRET")
    headers = {"secret": secret}

    try:
        key = f"{payload.project_id}/{payload.file_id}/{payload.file_name}"
        print(f"DEBUG: Starting embedding task for key: {key}")
        chunks = get_chunks_from_s3_file(key)
        print(f"DEBUG: Retrieved {len(chunks)} chunks")
        try:
            collection = chroma_client.get_or_create_collection(str(payload.project_id))
        except Exception as e:
            print(f"Collection failed to be created: {e}")
            url = f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/fail-process"
            httpx.post(url, headers=headers)
            return
        
        if len(chunks) == 0 or not chunks:
            print("No chunks found")
            url = f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/fail-process"
            httpx.post(url, headers=headers)
            return

        for idx, chunk in enumerate(chunks):
            collection.add(
                ids=[f"{key}_chunk_{idx}"],
                documents=[chunk],
                metadatas=[{
                    "project_id": str(payload.project_id),
                    "file_id": str(payload.file_id),
                    "filename": payload.file_name
                }]
            )
        print("DEBUG: Successfully added embeddings to Chroma")
        
        url = f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/confirm-process"
        
        print(f"DEBUG: Sending POST to: {url}")
        r = httpx.post(url, headers=headers)
        print(f"DEBUG: Confirm-process response: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"DEBUG EXCEPTION in embed_file_task: {e}")
        import traceback
        traceback.print_exc()
        try:
            url = f"{backend_url}/project/{payload.project_id}/file/{payload.file_id}/fail-process"
            httpx.post(url, headers=headers)
        except Exception as callback_err:
            print(f"DEBUG: Failed to send failure callback: {callback_err}")