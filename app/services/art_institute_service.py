import httpx
from typing import Any, Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings


class ArtInstituteService:
    """Service for interacting with Art Institute of Chicago API."""

    BASE_URL = settings.ART_INSTITUTE_API_URL
    TIMEOUT = settings.ART_INSTITUTE_TIMEOUT

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=self.TIMEOUT,
            headers={"User-Agent": "Travel-Planner/1.0"},
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_artwork(self, artwork_id: int) -> Optional[Dict[str, Any]]:
        """Get artwork by ID."""
        try:
            response = await self.client.get(f"/artworks/{artwork_id}")
            response.raise_for_status()
            data = response.json()
            return data.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            raise Exception(f"Failed to fetch artwork {artwork_id}: {str(e)}")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def search_artworks(
        self, query: str, limit: int = 10, page: int = 1
    ) -> List[Dict[str, Any]]:
        """Search artworks by query."""
        try:
            response = await self.client.get(
                "/artworks/search",
                params={
                    "q": query,
                    "limit": limit,
                    "page": page,
                    "fields": "id,title,artist_title,date_display,image_id,thumbnail",
                },
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            raise Exception(f"Failed to search artworks: {str(e)}")

    async def validate_artwork_exists(self, artwork_id: int) -> bool:
        """Check if artwork exists in API."""
        artwork = await self.get_artwork(artwork_id)
        return artwork is not None

    async def get_artworks_batch(self, artwork_ids: List[int]) -> List[Dict[str, Any]]:
        """Get multiple artworks by IDs."""
        artworks = []
        for artwork_id in artwork_ids:
            artwork = await self.get_artwork(artwork_id)
            if artwork:
                artworks.append(artwork)
        return artworks

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


async def get_art_institute_service():
    """Dependency to get ArtInstituteService instance."""
    service = ArtInstituteService()
    try:
        yield service
    finally:
        await service.close()
