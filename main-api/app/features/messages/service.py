import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.core.db import Message as MessageModel, Project as ProjectModel, SenderType
from app.features.messages.schemas import PostUserMessageDTO

class MessageService:
    @staticmethod
    def get_all_project_messages(
        session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID
    ) -> list[MessageModel]:
        project = session.exec(
            select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        all_messages = session.exec(
            select(MessageModel).where(MessageModel.project_id == project_id)
        ).all()
        return all_messages

    @staticmethod
    def post_ai_project_message(
        session: Session,
        project_id: uuid.UUID,
        payload: PostUserMessageDTO
    ) -> MessageModel:
        project = session.exec(
            select(ProjectModel).where(ProjectModel.id == project_id)
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        new_message = MessageModel(
            content=payload.content,
            sender=SenderType.AI,
            project_id=project_id
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        return new_message

    @staticmethod
    def post_user_project_message(
        session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID,
        payload: PostUserMessageDTO
    ) -> MessageModel:
        project = session.exec(
            select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)
        ).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        new_message = MessageModel(
            content=payload.content,
            sender=SenderType.USER,
            project_id=project_id
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        return new_message
