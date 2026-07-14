from __future__ import annotations
import os

from fastapi import Depends, Header, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign_in/")

async def get_user_id(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token)['id']

async def get_internal_secret(secret_key: str = Header(default=None)):
    expected_secret = os.getenv("INTERNAL_API_SECRET")
    if not secret_key or secret_key != expected_secret:
        raise HTTPException(status_code=403, detail="Unauthorized internal request")
    return secret_key

