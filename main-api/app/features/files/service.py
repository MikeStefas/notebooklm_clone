import os
import uuid
from loguru import logger
from sqlmodel import Session
from fastapi import HTTPException
from app.core.db import Project as ProjectModel, File as FileModel, FileStatus
from app.core.minio_client import delete_from_minio, create_presigned_get_url, create_presigned_post
from app.core.embedding_api__requests import request_embed, EmbedFileDTO, request_delete, DeleteEmbeddingsDTO
from app.helpers.validate_db import validate_project_access, validate_file_access, validate_project_exists

BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "file_storage")

class FileService:
    @staticmethod
    async def get_minio_presigned_post(session: Session, user_id: str | uuid.UUID, project_id: uuid.UUID, filename: str, content_type: str) -> dict:
        
        project = validate_project_access(session, user_id, project_id)
        
        if not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        new_file = FileModel(
            name=filename,
            project_id=project_id,
            nextcloud_path=f"/projects/{project_id}/{filename}"
        )

        key = f"{project_id}/{new_file.id}/{filename}"
        content_type = content_type or "application/octet-stream"
        post_data = create_presigned_post(BUCKET_NAME, key, content_type=content_type)

        if not post_data:
            raise HTTPException(status_code=500, detail="Upload failed")

        try:
            session.add(new_file)
            session.commit()
            session.refresh(new_file)
        except Exception as e:
            session.rollback()
            delete_from_minio(project_id, new_file.id, BUCKET_NAME)
            raise HTTPException(status_code=500, detail="Failed to write to db")

        return {
            "file_created": new_file,
            "url": post_data["url"],
            "fields": post_data["fields"]
        }

    @staticmethod
    async def delete_file_from_project(
        session: Session, 
        user_id: str | uuid.UUID, 
        project_id: uuid.UUID, 
        file_id: uuid.UUID
    ) -> FileModel:
        
        project = validate_project_access(session, user_id, project_id)
        
        selected_file = validate_file_access(session, project_id, file_id)
        file_snapshot = selected_file

        # Finish all DB work first
        try:
            session.delete(selected_file)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Failed to delete file from database")

        # HTTP calls after session is clean
        delete_from_minio(project_id, file_id, BUCKET_NAME)
        await request_delete(DeleteEmbeddingsDTO(project_id=project_id, file_id=file_id))

        return file_snapshot

    @staticmethod
    def get_file_presigned_url(
        session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID,
        file_id: uuid.UUID
    ) -> str:
        project = validate_project_access(session, user_id, project_id)
        
        selected_file = validate_file_access(session, project_id, file_id)
            
        key = f"{project_id}/{file_id}/{selected_file.name}"
        presigned_url = create_presigned_get_url(BUCKET_NAME, key)
        if not presigned_url:
            raise HTTPException(status_code=500, detail="Failed to generate presigned URL")
            
        return presigned_url

    @staticmethod
    async def confirm_upload(session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID,
        file_id: uuid.UUID) -> FileModel:

        project = validate_project_access(session, user_id, project_id)
        
        selected_file = validate_file_access(session, project_id, file_id)
        
        selected_file.status = FileStatus.PROCESSING
        session.add(selected_file)
        session.commit()
        session.refresh(selected_file)
        file_name = selected_file.name

        # HTTP call after all DB work is done
        try:
            await request_embed(EmbedFileDTO(project_id=project_id, file_id=file_id, file_name=file_name))
        except Exception as e:
            logger.exception(f"Error triggering embedding service: {e}")
            selected_file.status = FileStatus.FAILED
            session.add(selected_file)
            session.commit()
            session.refresh(selected_file)
            raise HTTPException(status_code=500, detail=f"Failed to trigger embedding service: {str(e)}")
        
        return selected_file

    @staticmethod
    def start_process(session: Session,
        project_id: uuid.UUID,
        file_id: uuid.UUID) -> FileModel:

        project = validate_project_exists(session, project_id)
        
        selected_file = validate_file_access(session, project_id, file_id)
        
        selected_file.status = FileStatus.PROCESSING
        
        session.add(selected_file)
        session.commit()
        session.refresh(selected_file)
        return selected_file

    @staticmethod
    def confirm_process(session: Session,
        project_id: uuid.UUID,
        file_id: uuid.UUID) -> FileModel:

        project = validate_project_exists(session, project_id)
        
        selected_file = validate_file_access(session, project_id, file_id)
        
        selected_file.status = FileStatus.PROCESSED
        
        session.add(selected_file)
        session.commit()
        session.refresh(selected_file)
        return selected_file
    
    @staticmethod
    def fail_process(session: Session,
        project_id: uuid.UUID,
        file_id: uuid.UUID) -> FileModel:

        project = validate_project_exists(session, project_id)
        
        selected_file = validate_file_access(session, project_id, file_id)
        
        selected_file.status = FileStatus.FAILED
        
        session.add(selected_file)
        session.commit()
        session.refresh(selected_file)
        return selected_file