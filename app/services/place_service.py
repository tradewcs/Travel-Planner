from typing import List, Optional, Dict, Any
from uuid import UUID

from app.repositories.place_repository import PlaceRepository
from app.repositories.project_place_repository import ProjectPlaceRepository
from app.services.art_institute_service import ArtInstituteService
from app.db.models import Place


class PlaceService:
    """Service for place-related business logic."""

    def __init__(
        self,
        place_repo: PlaceRepository,
        project_place_repo: ProjectPlaceRepository,
        art_service: ArtInstituteService,
    ):
        self.place_repo = place_repo
        self.project_place_repo = project_place_repo
        self.art_service = art_service

    async def get_or_create_place_from_api(self, artwork_id: int) -> Optional[Place]:
        """Get existing place or create from API data."""
        existing = await self.place_repo.get_by_external_id(str(artwork_id))
        if existing:
            return existing

        artwork_data = await self.art_service.get_artwork(artwork_id)
        if not artwork_data:
            return None

        place = Place.from_api_response(artwork_data)
        return await self.place_repo.add(place)

    async def search_available_places(
        self, query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for places in external API."""
        return await self.art_service.search_artworks(query, limit)

    async def validate_place_exists(self, artwork_id: int) -> bool:
        """Validate place exists in external API."""
        return await self.art_service.validate_artwork_exists(artwork_id)

    async def get_place_by_id(self, place_id: UUID) -> Optional[Place]:
        """Get place by UUID."""
        return await self.place_repo.get(place_id)

    async def get_place_by_external_id(self, external_id: str) -> Optional[Place]:
        """Get place by external ID."""
        return await self.place_repo.get_by_external_id(external_id)
