from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from app.api.dependencies import get_place_service
from app.services.place_service import PlaceService
from app.schemas.place import ArtworkSearchResult, PlaceInDB
from app.schemas.api_responses import APIResponse

router = APIRouter(prefix="/places", tags=["places"])


@router.get("/search", response_model=APIResponse[List[ArtworkSearchResult]])
async def search_places(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    place_service: PlaceService = Depends(get_place_service)
):
    """Search for places in Art Institute of Chicago API."""
    try:
        results = await place_service.search_available_places(query=q, limit=limit)
        return APIResponse(data=[ArtworkSearchResult(**r) for r in results])
    except Exception:
        raise HTTPException(status_code=503, detail="External API unavailable")


@router.get("/{external_id}", response_model=APIResponse[PlaceInDB])
async def get_place_by_external_id(
    external_id: str,
    place_service: PlaceService = Depends(get_place_service)
):
    """Get a place by its external ID."""
    place = await place_service.get_place_by_external_id(external_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return APIResponse(data=PlaceInDB.model_validate(place))


@router.get("/internal/{place_id}", response_model=APIResponse[PlaceInDB])
async def get_place_by_uuid(
    place_id: UUID,
    place_service: PlaceService = Depends(get_place_service)
):
    """Get a place by internal UUID."""
    place = await place_service.get_place_by_id(place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    return APIResponse(data=PlaceInDB.model_validate(place))
