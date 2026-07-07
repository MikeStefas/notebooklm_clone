from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.features.auth.schemas import SignUpDTO, SignInDTO
from app.features.auth.service import AuthService

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/sign_up/")
async def sign_up(payload: SignUpDTO, session: Session = Depends(get_session)):
    return AuthService.create_user(session, payload)


@router.post("/sign_in/")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    payload = SignInDTO(email=form_data.username, password=form_data.password)
    return AuthService.sign_in(session, payload)
