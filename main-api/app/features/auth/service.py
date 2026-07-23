from fastapi import Cookie
from fastapi import HTTPException
from sqlmodel import Session, select
from app.core.db import User as UserModel
from app.features.auth.schemas import SignUpDTO, SignInDTO, TokenResponse
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError
from app.core.jwt import create_access_token, create_refresh_token, decode_refresh_token, JWT

#init module 
password_hash = PasswordHash.recommended()

class AuthService:
    @staticmethod
    def sign_up(session: Session, payload: SignUpDTO) -> TokenResponse:
        hashed_password = password_hash.hash(payload.password)
        
        username = payload.username
        user = UserModel(email=payload.email, hashed_password=hashed_password, username=username)
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")
        session.refresh(user)
        
        token_payload = JWT(email=user.email, id=user.id, username=user.username)
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def sign_in(session: Session, payload: SignInDTO) -> TokenResponse:
        
        user = session.exec(select(UserModel).where(UserModel.email == payload.email)).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
        is_valid = password_hash.verify(payload.password, user.hashed_password)
        
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if user.id is None:
            raise HTTPException(status_code=500, detail="User ID is missing")

        token_payload = JWT(email=user.email, id=user.id, username=user.username)
        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    def refresh_tokens(session: Session, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_refresh_token(refresh_token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        user = session.exec(select(UserModel).where(UserModel.id == payload["id"])).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        token_payload = JWT(email=user.email, id=user.id, username=user.username)
        access_token = create_access_token(token_payload)
        new_refresh_token = create_refresh_token(token_payload)

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)


