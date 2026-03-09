from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List
from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    place_ids: Optional[List[int]] = Field(None, description="Art Institute artwork IDs")


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    start_date: Optional[date] = None


class ProjectInDB(ProjectBase):
    id: UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    places_count: int = 0
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class ProjectList(BaseModel):
    items: List[ProjectInDB]
    total: int
    skip: int
    limit: int
