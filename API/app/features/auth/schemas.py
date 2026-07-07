from typing import TypedDict
from pydantic import BaseModel
from pydantic import EmailStr
from sqlmodel import SQLModel


class SignInDTO(SQLModel):
    email: EmailStr
    password : str


class SignUpDTO(SQLModel):
    email: EmailStr
    password: str


class TokenResponse(TypedDict):
    access_token: str
    refresh_token: str

