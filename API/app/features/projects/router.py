

from app.core.db import File as FileModel
import uuid
from fastapi import UploadFile, File
from app.core.db import Project as ProjectModel
from app.core.db import get_session
from app.core.dependencies import get_user_id
from fastapi import Depends, HTTPException
from sqlmodel import Session
from fastapi import APIRouter
from app.features.projects.schemas import PostProjectDTO, PostFileToProjectDTO, GetAllProjectsResponse, GetProjectByIdResponse
from app.features.projects.service import ProjectService

router = APIRouter(
    prefix="/project",
    tags=["Projects"],
)


@router.post("/")
async def post_project(
    payload: PostProjectDTO,
    user_id: str = Depends(get_user_id), 
    session: Session = Depends(get_session)
) -> ProjectModel:
    return ProjectService.post_project(session, payload, user_id)


@router.get("/", response_model=list[GetAllProjectsResponse])
async def get_all_projects(
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session)
) -> list[GetAllProjectsResponse]:
    return ProjectService.get_all_projects(session, user_id)



@router.get("/{project_id}", response_model=GetProjectByIdResponse)
async def get_project_by_id(
    project_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session)
) -> GetProjectByIdResponse:
    project = ProjectService.get_project_by_id(session, user_id, project_id)

    return project

@router.post("/{project_id}/file")
async def post_file_to_project(
    project_id: uuid.UUID,
    file: UploadFile,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> FileModel:
    return await ProjectService.post_file_to_project(session, user_id, project_id, file)

@router.delete("/{project_id}/file/{file_id}")
async def delete_file_from_project(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> FileModel:
    return ProjectService.delete_file_from_project(session, user_id, project_id, file_id)

@router.get("/{project_id}/file/{file_id}/presigned-url")
async def get_file_presigned_url(
    project_id: uuid.UUID,
    file_id: uuid.UUID,
    user_id: str = Depends(get_user_id),
    session: Session = Depends(get_session),
) -> dict:
    url = ProjectService.get_file_presigned_url(session, user_id, project_id, file_id)
    return {"url": url}