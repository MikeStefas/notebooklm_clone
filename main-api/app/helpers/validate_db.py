import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.core.db import Project as ProjectModel, File as FileModel, Message as MessageModel


def validate_project_access(session: Session, user_id: str | uuid.UUID, project_id: uuid.UUID) -> ProjectModel:
    project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


def validate_project_exists(session: Session, project_id: uuid.UUID) -> ProjectModel:
    project = session.exec(select(ProjectModel).where(ProjectModel.id == project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def validate_file_access(session: Session, project_id: uuid.UUID, file_id: uuid.UUID) -> FileModel:
    selected_file = session.exec(select(FileModel).where(FileModel.id == file_id, FileModel.project_id == project_id)).first()
        
    if not selected_file:
        raise HTTPException(status_code=404, detail="File not found")

    return selected_file


def validate_message_access(session: Session, project_id: uuid.UUID) -> list[MessageModel]:
    messages = session.exec(
            select(MessageModel).where(MessageModel.project_id == project_id)
        ).all()
    return list(messages)