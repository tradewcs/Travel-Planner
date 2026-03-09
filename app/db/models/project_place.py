from typing import Optional
from uuid import UUID
from sqlalchemy import Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.types import DateTimeUTC

from app.db.models.project import ProjectStatus
from app.db.models.base import BaseModel


class ProjectPlace(BaseModel):
    """Association model between Project and Place with additional fields."""

    __tablename__ = "project_places"
    __table_args__ = (
        UniqueConstraint("project_id", "place_id", name="uq_project_place"),
    )

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    place_id: Mapped[UUID] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"), nullable=False, index=True
    )

    notes: Mapped[Optional[str]] = mapped_column(Text)
    visited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    visited_at: Mapped[Optional[DateTimeUTC]] = mapped_column(DateTimeUTC)

    order_index: Mapped[Optional[int]] = mapped_column()

    project: Mapped["Project"] = relationship(
        "Project", back_populates="project_places"
    )
    place: Mapped["Place"] = relationship(
        "Place", back_populates="project_places", lazy="selectin"
    )

    def mark_visited(self) -> None:
        """Mark this place as visited."""
        from datetime import datetime, timezone

        self.visited = True
        self.visited_at = datetime.now(timezone.utc)

        if self.project and self.project.is_completed:
            self.project.status = ProjectStatus.COMPLETED

    def __repr__(self) -> str:
        return f"<ProjectPlace(project={self.project_id}, place={self.place_id}, visited={self.visited})>"
