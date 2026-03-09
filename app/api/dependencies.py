from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.project_repository import ProjectRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.project_place_repository import ProjectPlaceRepository
from app.services.project_service import ProjectService
from app.services.place_service import PlaceService
from app.services.art_institute_service import ArtInstituteService, get_art_institute_service


async def get_db_session() -> AsyncSession:
    """Get database session."""
    async for session in get_session():
        yield session


async def get_project_repository(
    session: AsyncSession = Depends(get_db_session)
) -> ProjectRepository:
    """Get project repository."""
    return ProjectRepository(session=session)


async def get_place_repository(
    session: AsyncSession = Depends(get_db_session)
) -> PlaceRepository:
    """Get place repository."""
    return PlaceRepository(session=session)


async def get_project_place_repository(
    session: AsyncSession = Depends(get_db_session)
) -> ProjectPlaceRepository:
    """Get project place repository."""
    return ProjectPlaceRepository(session=session)

async def get_place_service(
    place_repo: PlaceRepository = Depends(get_place_repository),
    project_place_repo: ProjectPlaceRepository = Depends(get_project_place_repository),
    art_service: ArtInstituteService = Depends(get_art_institute_service)
) -> PlaceService:
    """Get place service."""
    return PlaceService(
        place_repo=place_repo,
        project_place_repo=project_place_repo,
        art_service=art_service
    )

async def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repository),
    project_place_repo: ProjectPlaceRepository = Depends(get_project_place_repository),
    place_service: PlaceService = Depends(get_place_service)
) -> ProjectService:
    """Get project service."""
    return ProjectService(
        project_repo=project_repo,
        project_place_repo=project_place_repo,
        place_service=place_service
    )

# Placeholder for auth
async def get_current_user():
    """Get current authenticated user (bonus feature)."""
    # Return dummy user for now
    return {"id": "user123", "username": "testuser"}
