from __future__ import annotations
import os

from fastapi import Depends, Header, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign_in")

async def get_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        if not payload or 'id' not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return payload['id']
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

async def get_internal_secret(secret: str = Header(default=None)):
    expected_secret = os.getenv("INTERNAL_API_SECRET")
    if not secret or secret != expected_secret:
        raise HTTPException(status_code=403, detail="Unauthorized internal request")
    return secret

