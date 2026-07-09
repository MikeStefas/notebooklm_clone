import uuid
from sqlmodel import Session, select
from fastapi import HTTPException
from app.core.db import Project as ProjectModel
from app.features.projects.schemas import PostProjectDTO, GetAllProjectsResponse, GetProjectByIdResponse


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