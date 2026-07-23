import os
import uuid
from sqlmodel import Session, select
from fastapi import HTTPException, UploadFile
from app.core.db import Project as ProjectModel, File as FileModel, FileStatus
from app.core.minio_client import upload_to_minio, delete_from_minio, create_presigned_get_url, create_presigned_post
from app.core.embedding_api__requests import request_embed, EmbedFileDTO, request_delete, DeleteEmbeddingsDTO


BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "file_storage")

class FileService:
    @staticmethod
    async def get_minio_presigned_post(session: Session, user_id: str | uuid.UUID, project_id: uuid.UUID, filename: str, content_type: str) -> dict:
        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        new_file = FileModel(
            name=filename,
            project_id=project_id,
            nextcloud_path=f"/projects/{project_id}/{filename}"
        )

        session.add(new_file)
        
        key = f"{project_id}/{new_file.id}/{filename}"
        content_type = content_type or "application/octet-stream"
        post_data = create_presigned_post(BUCKET_NAME, key, content_type=content_type)

        if post_data:
            try:
                session.commit()
                session.refresh(new_file)
            except Exception as e:
                session.rollback()
                delete_from_minio(project_id, new_file.id, BUCKET_NAME)
                raise HTTPException(status_code=500, detail="Failed to write to db")
        else:
            session.rollback()
            raise HTTPException(status_code=500, detail="Upload failed")

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
        
        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        selected_file = session.exec(select(FileModel).where(FileModel.id == file_id, FileModel.project_id == project_id)).first()
        
        if not selected_file:
            raise HTTPException(status_code=404, detail="File not found")
            
        delete_success = delete_from_minio(project_id, file_id, BUCKET_NAME)
        if delete_success:
            try:
                try:
                    await request_delete(DeleteEmbeddingsDTO(project_id=project_id, file_id=file_id))
                except HTTPException as he:
                    if he.status_code != 404:
                        raise he
                session.delete(selected_file)
                session.commit()
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=500, detail="Failed to delete file from database")
        else:
            session.rollback()
            raise HTTPException(status_code=500, detail="Delete from minio failed")

        return selected_file

    @staticmethod
    def get_file_presigned_url(
        session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID,
        file_id: uuid.UUID
    ) -> str:
        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        selected_file = session.exec(select(FileModel).where(FileModel.id == file_id, FileModel.project_id == project_id)).first()
        if not selected_file:
            raise HTTPException(status_code=404, detail="File not found")
            
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

        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        selected_file = session.exec(select(FileModel).where(FileModel.id == file_id, FileModel.project_id == project_id)).first()
        if not selected_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        selected_file.status = FileStatus.UPLOADED
        session.commit()
        
        session.add(selected_file)
        session.refresh(selected_file)
        try:
            await request_embed(EmbedFileDTO(project_id=project_id, file_id=file_id, file_name=selected_file.name))
        except Exception as e:
            selected_file.status = FileStatus.FAILED
            session.add(selected_file)
            session.commit()
            session.refresh(selected_file)
            raise HTTPException(status_code=500, detail="Failed to trigger embedding service")
        
        return selected_file
    
    @staticmethod
    def confirm_process(session: Session,
        project_id: uuid.UUID,
        file_id: uuid.UUID) -> FileModel:

        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id)).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        selected_file = session.exec(select(FileModel).where(FileModel.id == file_id, FileModel.project_id == project_id)).first()
        if not selected_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        selected_file.status = FileStatus.PROCESSED
        
        session.add(selected_file)
        session.commit()
        session.refresh(selected_file)
        return selected_file
    
    @staticmethod
    def fail_process(session: Session,
        project_id: uuid.UUID,
        file_id: uuid.UUID) -> FileModel:

        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id)).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        selected_file = session.exec(select(FileModel).where(FileModel.id == file_id, FileModel.project_id == project_id)).first()
        if not selected_file:
            raise HTTPException(status_code=404, detail="File not found")
        
        selected_file.status = FileStatus.FAILED
        
        session.add(selected_file)
        session.commit()
        session.refresh(selected_file)
        return selected_file