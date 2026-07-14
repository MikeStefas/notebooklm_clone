from typing import TypedDict, Optional
from pydantic import BaseModel
from pydantic import EmailStr
from sqlmodel import SQLModel


class SignInDTO(SQLModel):
    email: EmailStr
    password : str


class SignUpDTO(SQLModel):
    email: EmailStr
    password: str
    username: str


class TokenResponse(TypedDict):
    access_token: str
    refresh_token: str

class RefreshRequestDTO(SQLModel):
    refresh_token: str
