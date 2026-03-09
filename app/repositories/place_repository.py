from app.db.models import Place
from app.repositories.base import BaseRepository


class PlaceRepository(BaseRepository[Place]):
    """Repository for Place model."""

    model_type = Place

    async def get_by_external_id(self, external_id: str) -> Place | None:
        """Get a place by its external ID from the API."""
        return await self.get_one_or_none(external_id=external_id)

    async def get_or_create_from_api(self, api_data: dict) -> Place:
        """Get existing place or create new one from API data."""
        external_id = str(api_data.get("id"))
        existing = await self.get_by_external_id(external_id)

        if existing:
            return existing

        place = Place.from_api_response(api_data)
        return await self.add(place)
