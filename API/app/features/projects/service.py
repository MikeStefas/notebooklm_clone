import os
import uuid
from sqlmodel import Session, select
from fastapi import HTTPException, UploadFile
from app.core.db import Project as ProjectModel, File as FileModel
from app.features.projects.schemas import PostProjectDTO, PostFileToProjectDTO
from app.core.minio_client import upload_to_minio, delete_from_minio


BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "file_storage")

class ProjectService:
    @staticmethod
    def post_project(session: Session, payload: PostProjectDTO, user_id: str | uuid.UUID) -> ProjectModel:
        new_proj = ProjectModel(title=payload.title, user_id=user_id)
        session.add(new_proj)
        session.commit()
        session.refresh(new_proj)
        return new_proj

    @staticmethod
    def get_all_projects(session: Session, user_id: str | uuid.UUID) -> list[ProjectModel]:
        projects = session.exec(select(ProjectModel).where(ProjectModel.user_id == user_id)).all()
        return list(projects)

    @staticmethod
    def get_project_by_id(session: Session, user_id: str | uuid.UUID, project_id: str | uuid.UUID) -> ProjectModel | None:
        project = session.exec(select(ProjectModel).where(ProjectModel.user_id == user_id, ProjectModel.id == project_id)).first()
        return project
    
    @staticmethod
    async def post_file_to_project(session: Session, user_id: str | uuid.UUID, project_id: uuid.UUID, file: UploadFile) -> FileModel:
        project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        filename = file.filename or "unnamed"
        new_file = FileModel(
            name=filename,
            project_id=project_id,
            nextcloud_path=f"/projects/{project_id}/{filename}"
        )

        session.add(new_file)
        
            
        result = upload_to_minio(project_id, new_file.id, file, BUCKET_NAME)

        if result:
            try:
                session.commit()
                session.refresh(new_file)
            except Exception as e:
                session.rollback()
                delete_from_minio(project_id, new_file.id, BUCKET_NAME)
                raise HTTPException(status_code=500, detail=f"Failed to write to db")
        else:
            session.rollback()
            raise HTTPException(status_code=500, detail="Upload failed")

        return new_file

    @staticmethod
    def delete_file_from_project(
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
                session.delete(selected_file)
                session.commit()
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to delete file from database")
        else:
            session.rollback()
            raise HTTPException(status_code=500, detail="Delete from minio failed")

        return selected_file