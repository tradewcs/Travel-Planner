from typing import List, Optional
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class Place(BaseModel):
    """Place model representing artworks from Art Institute of Chicago API."""

    __tablename__ = "places"

    external_id: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    artist_title: Mapped[Optional[str]] = mapped_column(String(500))
    date_display: Mapped[Optional[str]] = mapped_column(String(200))
    main_reference_number: Mapped[Optional[str]] = mapped_column(String(100))

    api_data: Mapped[Optional[dict]] = mapped_column(JSON)

    image_id: Mapped[Optional[str]] = mapped_column(String(100))
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500))

    project_places: Mapped[List["ProjectPlace"]] = relationship(
        "ProjectPlace",
        back_populates="place",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @classmethod
    def from_api_response(cls, api_data: dict) -> "Place":
        """Create a Place instance from Art Institute API response."""
        return cls(
            external_id=str(api_data.get("id")),
            title=api_data.get("title", "Unknown Title"),
            artist_title=api_data.get("artist_title"),
            date_display=api_data.get("date_display"),
            main_reference_number=api_data.get("main_reference_number"),
            image_id=api_data.get("image_id"),
            thumbnail_url=(
                api_data.get("thumbnail", {}).get("lqip")
                if api_data.get("thumbnail")
                else None
            ),
            api_data=api_data,
        )

    def __repr__(self) -> str:
        return f"<Place(id={self.id}, title='{self.title[:50]}')>"
