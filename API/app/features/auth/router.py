from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.features.auth.schemas import SignUpDTO, SignInDTO, RefreshRequestDTO
from app.features.auth.service import AuthService
from app.features.auth.schemas import TokenResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/sign_up/")
async def sign_up(payload: SignUpDTO, session: Session = Depends(get_session)) -> TokenResponse:
    return AuthService.sign_up(session, payload)


@router.post("/sign_in/")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> TokenResponse:
    payload = SignInDTO(email=form_data.username, password=form_data.password)
    return AuthService.sign_in(session, payload)

@router.post("/refresh/")
async def refresh_token(payload: RefreshRequestDTO, session: Session = Depends(get_session)) -> TokenResponse:
    return AuthService.refresh_tokens(session, payload.refresh_token)