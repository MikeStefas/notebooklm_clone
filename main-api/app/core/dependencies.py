from __future__ import annotations

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign_in/")

async def get_user_id(token: str = Depends(oauth2_scheme)):
    return decode_access_token(token)['id']
