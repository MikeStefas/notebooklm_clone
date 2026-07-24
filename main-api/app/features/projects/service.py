import uuid
from sqlmodel import Session, select
from fastapi import HTTPException
from app.core.db import Project as ProjectModel, FileStatus
from app.features.projects.schemas import PostProjectDTO, GetAllProjectsResponse, GetProjectByIdResponse
from app.helpers.validate_db import validate_project_access

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
            processed_file_count = 0
            for file in project.files:
                if file.status == FileStatus.PROCESSED:
                    processed_file_count += 1
            project_responses.append(GetAllProjectsResponse(
                id=project.id,
                user_id=project.user_id,
                title=project.title,
                created_at=project.created_at,
                updated_at=project.updated_at,
                file_count=processed_file_count
            ))
        return project_responses

    @staticmethod
    def get_project_by_id(session: Session, user_id: str | uuid.UUID, project_id: str | uuid.UUID) -> GetProjectByIdResponse:
        project = validate_project_access(session, user_id, project_id)
        
        processed_files = []
        for file in project.files:
            if file.status == FileStatus.PROCESSED:
                processed_files.append(file)
        
        return GetProjectByIdResponse(
            id=project.id,
            user_id=project.user_id,
            title=project.title,
            created_at=project.created_at,
            updated_at=project.updated_at,
            file_count=len(processed_files),
            files=processed_files 
        )