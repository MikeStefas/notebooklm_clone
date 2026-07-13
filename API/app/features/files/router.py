import uuid
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session
from app.core.db import get_session
from app.core.dependencies import get_user_id
from app.features.files.service import FileService
from app.features.files.schemas import FileResponse, PresignedUrlResponse, FilePresignedUploadResponse

router = APIRouter(
    prefix="/project/{project_id}/file",
    tags=["Files"],
)

@router.post("/upload", response_model=FilePresignedUploadResponse)
async def get_minio_put_url(
    project_id: uuid.UUID,
    file: UploadFile,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> FilePresignedUploadResponse:
    return await FileService.get_minio_presigned_post(session, user_id, project_id, file)

@router.delete("/{file_id}", response_model=FileResponse)
async def delete_file_from_project(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> FileResponse:
    return FileService.delete_file_from_project(session, user_id, project_id, file_id)

@router.get("/{file_id}/presigned-url", response_model=PresignedUrlResponse)
async def get_file_presigned_url(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> PresignedUrlResponse:
    url = FileService.get_file_presigned_url(session, user_id, project_id, file_id)
    return PresignedUrlResponse(url=url)

