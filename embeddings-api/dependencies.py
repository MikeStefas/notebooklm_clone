import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

CHROMA_DATA_PATH = os.getenv("CHROMA_DATA_PATH", "./chroma_data")


def create_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_DATA_PATH)


def get_chroma_collection(chroma_client, project_id: str, task_type: str = "RETRIEVAL_DOCUMENT") -> chromadb.Collection:
    google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
        model_name="gemini-embedding-001",
        task_type=task_type,
    )
    return chroma_client.get_or_create_collection(
        name=project_id,
        embedding_function=google_ef
    )
