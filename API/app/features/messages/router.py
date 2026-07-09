
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.db import get_session, Message as MessageModel, Project as ProjectModel, SenderType
from app.core.dependencies import get_user_id
from app.features.messages.schemas import PostUserMessageDTO, MessageResponse

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
    project = session.exec(
        select(ProjectModel).where(ProjectModel.id == project_id, ProjectModel.user_id == user_id)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    all_messages = session.exec(
        select(MessageModel).where(MessageModel.project_id == project_id)
    ).all()
    return all_messages


@router.post("/", response_model=MessageResponse)
async def post_project_message(
    project_id: uuid.UUID,
    payload: PostUserMessageDTO,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
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

