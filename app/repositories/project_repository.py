from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Project, ProjectPlace, ProjectStatus
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model."""

    model_type = Project

    async def get_with_places(self, project_id: UUID) -> Project | None:
        """Get project with all its places eagerly loaded."""
        stmt = (
            select(Project)
            .where(Project.id == project_id)
            .options(
                selectinload(Project.project_places).selectinload(ProjectPlace.place)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_projects(self) -> list[Project]:
        """Get all active projects."""
        return await self.list(status=ProjectStatus.ACTIVE)

    async def complete_project(self, project_id: UUID) -> Project | None:
        """Mark a project as completed."""
        project = await self.get(project_id)
        if project:
            project.status = ProjectStatus.COMPLETED  # Use enum
            project = await self.update(project)
        return project
