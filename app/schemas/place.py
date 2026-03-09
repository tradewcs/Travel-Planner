from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Any, Dict


class PlaceBase(BaseModel):
    external_id: str
    title: str
    artist_title: Optional[str] = None
    date_display: Optional[str] = None
    image_id: Optional[str] = None
    thumbnail_url: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class PlaceInDB(PlaceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArtworkSearchResult(BaseModel):
    id: int
    title: str
    artist_title: Optional[str] = None
    date_display: Optional[str] = None
    image_id: Optional[str] = None
    thumbnail: Optional[Dict[str, Any]] = None
