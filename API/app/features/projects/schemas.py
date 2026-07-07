
from sqlmodel import SQLModel

class PostProjectDTO(SQLModel):
    title : str

class PostFileToProjectDTO(SQLModel):
    title: str
