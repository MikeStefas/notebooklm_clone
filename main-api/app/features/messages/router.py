
import uuid
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session, Message as MessageModel
from app.core.dependencies import get_user_id, get_internal_secret
from app.features.messages.schemas import PostUserMessageDTO, MessageResponse
from app.features.messages.service import MessageService

router = APIRouter(
    prefix="/project/{project_id}/messages",
    tags=["Messages"],
)

@router.get("/", response_model=list[MessageResponse])
async def get_all_project_messages(
    project_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> list[MessageModel]:
    return MessageService.get_all_project_messages(session, user_id, project_id)


@router.post("/ai", response_model=MessageResponse)
async def post_ai_project_message(
    project_id: uuid.UUID,
    payload: PostUserMessageDTO,
    session: Session = Depends(get_session),
    secret: str = Depends(get_internal_secret)
) -> MessageModel:
    return MessageService.post_ai_project_message(session, project_id, payload)

@router.post("/user", response_model=list[str])
async def post_user_project_message(
    project_id: uuid.UUID,
    payload: PostUserMessageDTO,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> list[str]:
    return await MessageService.post_user_project_message(session, user_id, project_id, payload)
