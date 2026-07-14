# Embeddings & Vector DB API

A dedicated FastAPI microservice for managing text embeddings and vector storage using **ChromaDB** and **SentenceTransformers**.

## Features

- **Text Embeddings**: Generate raw vectors from text using SentenceTransformer models (default: `all-MiniLM-L6-v2`).
- **ChromaDB Collection Management**: Create, list, describe, and delete collections.
- **Document Management**: Add text documents, generate their embeddings automatically, and store them with custom IDs and metadatas.
- **Vector Querying**: Query collections with natural language query strings to find similar document chunks.
- **Service Health Check**: Endpoint to check the connection to ChromaDB and verify if the embedding model is loaded.

## Getting Started

### Prerequisites

This service runs on Python 3.12+ and has its own isolated virtual environment managed via `uv`.

### Running the API

To start the embeddings API locally on port `8001` (to avoid conflicting with the main app on `8000`), run the following command from the root of the `notebook-lm` project:

```bash
cd embeddings-api
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Alternatively, you can run it directly:

```bash
/home/mike/code/notebook-lm/embeddings-api/.venv/bin/uvicorn main:app --app-dir /home/mike/code/notebook-lm/embeddings-api --host 0.0.0.0 --port 8001
```

Once running, you can access the interactive API documentation at:
- Swagger UI: [http://localhost:8001/docs](http://localhost:8001/docs)
- ReDoc: [http://localhost:8001/redoc](http://localhost:8001/redoc)

## API Endpoints

### Health and Base

- `GET /`: Get service name and online status.
- `GET /health`: Check status of embedding model and ChromaDB connection.

### Embeddings

- `POST /embeddings`: Generate vector embeddings for a list of texts.
  - **Request Body**:
    ```json
    {
      "texts": ["Hello world", "Machine learning is fun"]
    }
    ```

### Collections

- `GET /collections`: List all available collections.
- `POST /collections`: Create a new collection.
  - **Request Body**:
    ```json
    {
      "name": "my-collection",
      "metadata": {
        "description": "Project documents"
      }
    }
    ```
- `GET /collections/{name}`: Get a collection's details and document count.
- `DELETE /collections/{name}`: Delete a collection.
- `POST /collections/{name}/documents`: Add documents to a collection (automatically embedded on addition).
  - **Request Body**:
    ```json
    {
      "documents": ["Text chunk 1", "Text chunk 2"],
      "metadatas": [{"source": "pdf1"}, {"source": "pdf2"}],
      "ids": ["doc_1", "doc_2"]
    }
    ```
- `POST /collections/{name}/query`: Search for similar documents in a collection.
  - **Request Body**:
    ```json
    {
      "query_text": "search query here",
      "n_results": 5,
      "where": { "source": "pdf1" }
    }
    ```
