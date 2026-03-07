from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models import ProjectPlace
from app.repositories.base import BaseRepository


class ProjectPlaceRepository(BaseRepository[ProjectPlace]):
    """Repository for ProjectPlace association model."""

    model_type = ProjectPlace

    async def get_project_places(self, project_id: UUID) -> list[ProjectPlace]:
        """Get all places for a specific project with place details."""
        stmt = (
            select(ProjectPlace)
            .where(ProjectPlace.project_id == project_id)
            .options(selectinload(ProjectPlace.place))
            .order_by(ProjectPlace.order_index)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_project_place(
        self, project_id: UUID, place_id: UUID
    ) -> ProjectPlace | None:
        """Get specific place within a project."""
        stmt = select(ProjectPlace).where(
            and_(
                ProjectPlace.project_id == project_id, ProjectPlace.place_id == place_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_place_to_project(
        self, project_id: UUID, place_id: UUID, notes: str | None = None
    ) -> ProjectPlace:
        """Add a place to a project."""
        project_place = ProjectPlace(
            project_id=project_id, place_id=place_id, notes=notes
        )
        return await self.add(project_place)

    async def update_notes(
        self, project_place_id: UUID, notes: str
    ) -> ProjectPlace | None:
        """Update notes for a project place."""
        project_place = await self.get(project_place_id)
        if project_place:
            project_place.notes = notes
            return await self.update(project_place)
        return None

    async def mark_as_visited(self, project_place_id: UUID) -> ProjectPlace | None:
        """Mark a place as visited."""
        project_place = await self.get(project_place_id)
        if project_place:
            project_place.mark_visited()
            return await self.update(project_place)
        return None

    async def count_project_places(self, project_id: UUID) -> int:
        """Count places in a project."""
        stmt = select(ProjectPlace).where(ProjectPlace.project_id == project_id)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    async def place_exists_in_project(self, project_id: UUID, place_id: UUID) -> bool:
        """Check if a place already exists in a project."""
        stmt = select(ProjectPlace).where(
            and_(
                ProjectPlace.project_id == project_id, ProjectPlace.place_id == place_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
