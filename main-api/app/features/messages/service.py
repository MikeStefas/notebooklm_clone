import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from app.core.db import Message as MessageModel, Project as ProjectModel, SenderType
from app.features.messages.schemas import PostUserMessageDTO
from app.helpers.validate_db import validate_project_access, validate_project_exists, validate_message_access
from app.core.embedding_api__requests import SearchDTO, request_search

from loguru import logger

class MessageService:
    @staticmethod
    def get_all_project_messages(
        session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID
    ) -> list[MessageModel]:
        validate_project_access(session, user_id, project_id)

        all_messages = validate_message_access(session, project_id)
        return all_messages

    @staticmethod
    def post_ai_project_message(
        session: Session,
        project_id: uuid.UUID,
        payload: PostUserMessageDTO
    ) -> MessageModel:
        project = validate_project_exists(session, project_id)
        
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
    async def post_user_project_message(
        session: Session,
        user_id: str | uuid.UUID,
        project_id: uuid.UUID,
        payload: PostUserMessageDTO
    ) -> list[str]:
        project = validate_project_access(session, user_id, project_id)

        new_message = MessageModel(
            content=payload.content,
            sender=SenderType.USER,
            project_id=project_id
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)

        search_payload = SearchDTO(
            prompt=payload.content,
            project_id=project_id,
        )
        search_result = await request_search(search_payload)
        
        logger.info(f"EMBEDDING SEARCH RESULT: {search_result}")
        print(f"\n--- EMBEDDING SEARCH RESULT FOR PROJECT {project_id} ---\n{search_result}\n----------------------------------------------------\n", flush=True)

        return search_result
