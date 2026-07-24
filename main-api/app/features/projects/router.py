

import uuid
from app.core.db import Project as ProjectModel
from app.core.db import get_session
from app.core.dependencies import get_user_id
from fastapi import Depends, HTTPException
from sqlmodel import Session
from fastapi import APIRouter
from app.features.projects.schemas import PostProjectDTO, GetAllProjectsResponse, GetProjectByIdResponse, GetProjectResponse, PostProjectResponse
from app.features.projects.service import ProjectService

router = APIRouter(
    prefix="/project",
    tags=["Projects"],
)


@router.post("/", response_model=PostProjectResponse)
async def post_project(
    payload: PostProjectDTO,
    user_id: str = Depends(get_user_id), 
    session: Session = Depends(get_session)
) -> PostProjectResponse:
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
    return ProjectService.get_project_by_id(session, user_id, project_id)