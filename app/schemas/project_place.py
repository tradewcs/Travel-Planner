from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.schemas.place import PlaceInDB


class ProjectPlaceBase(BaseModel):
    notes: Optional[str] = Field(None, max_length=5000)
    visited: bool = False


class ProjectPlaceCreate(ProjectPlaceBase):
    artwork_id: int = Field(..., description="Art Institute artwork ID")


class ProjectPlaceUpdate(BaseModel):
    notes: Optional[str] = Field(None, max_length=5000)
    visited: Optional[bool] = None


class ProjectPlaceInDB(ProjectPlaceBase):
    id: UUID
    project_id: UUID
    place_id: UUID
    visited_at: Optional[datetime] = None
    order_index: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectPlaceWithPlace(ProjectPlaceInDB):
    place: PlaceInDB
