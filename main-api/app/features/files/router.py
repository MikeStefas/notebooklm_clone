import uuid
from typing import Literal, Annotated
from fastapi import APIRouter, Depends, Header
from sqlmodel import Session
from app.core.db import get_session
from app.core.dependencies import get_user_id, get_internal_secret
from app.features.files.service import FileService
from app.features.files.schemas import FileResponse, PresignedUrlResponse, FilePresignedUploadResponse, PresignedUrlRequest

router = APIRouter(
    prefix="/project/{project_id}/file",
    tags=["Files"],
)

@router.post("/presigned-url", response_model=FilePresignedUploadResponse)
async def get_minio_presigned_post(
    project_id: uuid.UUID,
    req: PresignedUrlRequest,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> FilePresignedUploadResponse:
    return await FileService.get_minio_presigned_post(session, user_id, project_id, req.filename, req.content_type)

@router.delete("/{file_id}", response_model=FileResponse)
async def delete_file_from_project(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> FileResponse:
    return await FileService.delete_file_from_project(session, user_id, project_id, file_id)

@router.get("/{file_id}/presigned-url", response_model=PresignedUrlResponse)
async def get_file_presigned_url(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> PresignedUrlResponse:
    url = FileService.get_file_presigned_url(session, user_id, project_id, file_id)
    return PresignedUrlResponse(url=url)

@router.post("/{file_id}/confirm-upload")
async def confirm_upload(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
)-> FileResponse:
    return await FileService.confirm_upload(session, user_id, project_id, file_id)

@router.post("/{file_id}/confirm-process")
async def confirm_process(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    session: Session = Depends(get_session),
    secret: str = Depends(get_internal_secret)
) -> FileResponse:
    return FileService.confirm_process(session, project_id, file_id)

@router.post("/{file_id}/fail-process")
async def fail_process(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    session: Session = Depends(get_session),
    secret: str = Depends(get_internal_secret)
) -> FileResponse:
    return FileService.fail_process(session, project_id, file_id)
