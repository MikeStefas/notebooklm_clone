import os
import uuid
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, UploadFile
from app.core.db import Project as ProjectModel, File as FileModel
from app.features.projects.schemas import PostProjectDTO, PostFileToProjectDTO, GetAllProjectsResponse, GetProjectByIdResponse
from app.core.minio_client import upload_to_minio, delete_from_minio, create_presigned_url


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
    def get_all_projects(session: Session, user_id: str | uuid.UUID) -> list[GetAllProjectsResponse]:
        projects = session.exec(select(ProjectModel).where(ProjectModel.user_id == user_id)).all()
        project_responses= []
        for project in projects:
            project_responses.append(GetAllProjectsResponse(
                id=project.id,
                user_id=project.user_id,
                title=project.title,
                created_at=project.created_at,
                updated_at=project.updated_at,
                file_count=len(project.files) if project.files else 0
            ))
        return project_responses

    @staticmethod
    def get_project_by_id(session: Session, user_id: str | uuid.UUID, project_id: str | uuid.UUID) -> GetProjectByIdResponse:
        project = session.exec(select(ProjectModel).where(ProjectModel.user_id == user_id, ProjectModel.id == project_id)).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        file_count = len(project.files) if project.files else 0
        
        return GetProjectByIdResponse(
            id=project.id,
            user_id=project.user_id,
            title=project.title,
            created_at=project.created_at,
            updated_at=project.updated_at,
            file_count=file_count,
            files=project.files
        )
        
    
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
        presigned_url = create_presigned_url(BUCKET_NAME, key)
        if not presigned_url:
            raise HTTPException(status_code=500, detail="Failed to generate presigned URL")
            
        return presigned_url