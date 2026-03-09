from datetime import date
from enum import Enum
from typing import List, Optional
from sqlalchemy import String, Date, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class ProjectStatus(str, Enum):
    """Project status enum."""

    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(BaseModel):
    """Travel project model."""

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    description: Mapped[Optional[str]] = mapped_column(String(1000))
    start_date: Mapped[Optional[date]] = mapped_column(Date)

    status: Mapped[ProjectStatus] = mapped_column(
        SQLEnum(ProjectStatus), 
        default=ProjectStatus.ACTIVE,
        nullable=False, 
        index=True
    )

    project_places: Mapped[List["ProjectPlace"]] = relationship(
        "ProjectPlace",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def is_completed(self) -> bool:
        """Check if project is completed (all places visited)."""
        if not self.project_places:
            return False
        return all(pp.visited for pp in self.project_places)

    @property
    def places_count(self) -> int:
        """Get current number of places in project."""
        return len(self.project_places)

    def can_add_place(self) -> bool:
        """Check if a new place can be added (max 10)."""
        return self.places_count < 10

    def update_status_from_places(self) -> None:
        """Update project status based on places visited status."""
        if self.is_completed:
            self.status = ProjectStatus.COMPLETED
