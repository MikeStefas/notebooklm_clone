import os
import uuid
from sqlmodel import Session, select
from fastapi import HTTPException
from app.core.db import Project as ProjectModel, File as FileModel, FileStatus
from app.features.projects.schemas import PostProjectDTO, PostProjectResponse, GetAllProjectsResponse, GetProjectByIdResponse
from app.helpers.validate_db import validate_project_access
from app.core.minio_client import create_presigned_post, delete_from_minio

BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "file_storage")

class ProjectService:
    @staticmethod
    def post_project(session: Session, payload: PostProjectDTO, user_id: str | uuid.UUID) -> PostProjectResponse:
        new_proj = ProjectModel(title=payload.title, user_id=user_id)
        session.add(new_proj)
        session.commit()
        session.refresh(new_proj)

        created_file = None
        upload_url = None
        fields = None

        if payload.filename:
            new_file = FileModel(
                name=payload.filename,
                project_id=new_proj.id,
                nextcloud_path=f"/projects/{new_proj.id}/{payload.filename}",
                status=FileStatus.PENDING
            )
            session.add(new_file)
            session.commit()
            session.refresh(new_file)

            key = f"{new_proj.id}/{new_file.id}/{payload.filename}"
            content_type = payload.content_type or "application/octet-stream"
            post_data = create_presigned_post(BUCKET_NAME, key, content_type=content_type)

            if post_data:
                created_file = new_file
                upload_url = post_data["url"]
                fields = post_data["fields"]
            else:
                session.rollback()
                raise HTTPException(status_code=500, detail="Failed to create file upload URL")

        return PostProjectResponse(
            id=new_proj.id,
            user_id=new_proj.user_id,
            title=new_proj.title,
            created_at=new_proj.created_at,
            updated_at=new_proj.updated_at,
            file=created_file,
            upload_url=upload_url,
            fields=fields
        )

    @staticmethod
    def get_all_projects(session: Session, user_id: str | uuid.UUID) -> list[GetAllProjectsResponse]:
        projects = session.exec(select(ProjectModel).where(ProjectModel.user_id == user_id)).all()
        project_responses = []
        for project in projects:
            project_responses.append(GetAllProjectsResponse(
                id=project.id,
                user_id=project.user_id,
                title=project.title,
                created_at=project.created_at,
                updated_at=project.updated_at,
                file=project.file
            ))
        return project_responses

    @staticmethod
    def get_project_by_id(session: Session, user_id: str | uuid.UUID, project_id: str | uuid.UUID) -> GetProjectByIdResponse:
        project = validate_project_access(session, user_id, project_id)
        
        return GetProjectByIdResponse(
            id=project.id,
            user_id=project.user_id,
            title=project.title,
            created_at=project.created_at,
            updated_at=project.updated_at,
            file=project.file
        )