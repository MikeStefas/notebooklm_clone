from sqlalchemy import Boolean
from datetime import timedelta
from datetime import timezone
from datetime import datetime
from typing import TypedDict, cast
import uuid
from pydantic import EmailStr
import jwt
from app.core.config import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM


class JWT(TypedDict):
    email: EmailStr
    id: uuid.UUID | str
    username: str


def create_access_token(payload: JWT) -> str:
    data = {
        'email' : payload['email'],
        'id': str(payload['id']),
        'username': payload['username'],
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(payload: JWT) -> str:
    data = {
        'email' : payload['email'],
        'id': str(payload['id']),
        'username': payload['username'],
        'exp': datetime.now(timezone.utc) + timedelta(minutes=300)
    }
    return jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> JWT:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return JWT(
        email=payload["email"],
        id=uuid.UUID(payload["id"]), 
        username=payload["username"] 
    )


def decode_refresh_token(token: str) -> JWT:
    payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    return JWT(
        email=payload["email"],
        id=uuid.UUID(payload["id"]) , 
        username=payload["username"] 
    )

