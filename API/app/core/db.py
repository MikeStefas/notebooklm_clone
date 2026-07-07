from datetime import datetime, timezone
import uuid
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, create_engine, Relationship, Session


class User(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    # relationships
    user_projects: List["Project"] = Relationship(back_populates="user")


class Project(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID  = Field( foreign_key="user.id")
    title: str
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    # relationships
    user: User = Relationship(back_populates="user_projects")
    files: Optional[List["File"]] = Relationship(back_populates="project")


class File(SQLModel, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    project_id: uuid.UUID | None = Field(default=None, foreign_key="project.id")
    name: str
    nextcloud_path: str
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    # relationships
    project: Project = Relationship(back_populates="files")


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sqlite_file_path = BASE_DIR / "database.db"
sqlite_url = f"sqlite:///{sqlite_file_path}"

engine = create_engine(sqlite_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
