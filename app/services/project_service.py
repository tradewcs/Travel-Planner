from typing import List, Optional
from uuid import UUID
from datetime import date

from app.repositories.project_repository import ProjectRepository
from app.repositories.project_place_repository import ProjectPlaceRepository
from app.services.place_service import PlaceService
from app.models import Project, ProjectPlace, ProjectStatus
from app.core.config import settings
from app.core.exceptions import BusinessRuleViolation, ResourceNotFound


class ProjectService:
    """Service for project-related business logic."""

    def __init__(
        self,
        project_repo: ProjectRepository,
        project_place_repo: ProjectPlaceRepository,
        place_service: PlaceService,
    ):
        self.project_repo = project_repo
        self.project_place_repo = project_place_repo
        self.place_service = place_service
        self.max_places = settings.MAX_PLACES_PER_PROJECT

    async def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        place_ids: Optional[List[int]] = None,
    ) -> Project:
        """Create a new project with optional places."""
        project = Project(name=name, description=description, start_date=start_date)
        project = await self.project_repo.add(project)

        if place_ids:
            await self._add_places_to_project(project.id, place_ids)

        return project

    async def get_project(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID with places loaded."""
        return await self.project_repo.get_with_places(project_id)

    async def update_project(
        self,
        project_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
    ) -> Optional[Project]:
        """Update project details."""
        project = await self.project_repo.get(project_id)
        if not project:
            return None

        if name:
            project.name = name
        if description is not None:
            project.description = description
        if start_date is not None:
            project.start_date = start_date

        return await self.project_repo.update(project)

    async def delete_project(self, project_id: UUID) -> bool:
        """Delete project if no places are visited."""
        project = await self.project_repo.get_with_places(project_id)
        if not project:
            return False

        if any(pp.visited for pp in project.project_places):
            raise BusinessRuleViolation("Cannot delete project with visited places")

        await self.project_repo.delete(project_id)
        return True

    async def add_place_to_project(
        self, project_id: UUID, artwork_id: int
    ) -> Optional[ProjectPlace]:
        """Add a place to project."""
        project = await self.project_repo.get(project_id)
        if not project:
            raise ResourceNotFound(f"Project {project_id} not found")

        current_count = await self.project_place_repo.count_project_places(project_id)
        if current_count >= self.max_places:
            raise BusinessRuleViolation(
                f"Maximum {self.max_places} places per project allowed"
            )

        place = await self.place_service.get_or_create_place_from_api(artwork_id)
        if not place:
            raise ResourceNotFound(
                f"Artwork {artwork_id} not found in Art Institute API"
            )

        exists = await self.project_place_repo.place_exists_in_project(
            project_id, place.id
        )
        if exists:
            raise BusinessRuleViolation("Place already exists in this project")

        return await self.project_place_repo.add_place_to_project(project_id, place.id)

    async def update_place_in_project(
        self,
        project_id: UUID,
        place_id: UUID,
        notes: Optional[str] = None,
        visited: Optional[bool] = None,
    ) -> Optional[ProjectPlace]:
        """Update place details in project."""
        project_place = await self.project_place_repo.get_project_place(
            project_id, place_id
        )
        if not project_place:
            return None

        if notes is not None:
            project_place.notes = notes
            project_place = await self.project_place_repo.update(project_place)

        if visited:
            project_place = await self.project_place_repo.mark_as_visited(
                project_place.id
            )

            project = await self.project_repo.get_with_places(project_id)
            if project and project.is_completed:
                project.status = ProjectStatus.COMPLETED
                await self.project_repo.update(project)

        return project_place

    async def list_projects(
        self, skip: int = 0, limit: int = 100, status: Optional[ProjectStatus] = None
    ) -> List[Project]:
        """List projects with pagination and filtering."""
        filters = {}
        if status:
            filters["status"] = status

        return await self.project_repo.list(skip=skip, limit=limit, **filters)

    async def _add_places_to_project(
        self, project_id: UUID, artwork_ids: List[int]
    ) -> None:
        """Add multiple places to project (internal method)."""
        for artwork_id in artwork_ids:
            try:
                await self.add_place_to_project(project_id, artwork_id)
            except (ResourceNotFound, BusinessRuleViolation):
                continue
