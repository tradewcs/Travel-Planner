import pytest
from app.services.art_institute_service import ArtInstituteService


@pytest.mark.asyncio
async def test_search_artworks():
    service = ArtInstituteService()
    try:
        results = await service.search_artworks("monet", limit=5)
        
        assert isinstance(results, list)
        assert len(results) <= 5
        if results:
            assert "id" in results[0]
            assert "title" in results[0]
    finally:
        await service.close()


@pytest.mark.asyncio
async def test_get_artwork():
    service = ArtInstituteService()
    try:
        artwork = await service.get_artwork(27992)
        
        assert artwork is not None
        assert artwork["id"] == 27992
        assert "title" in artwork
    finally:
        await service.close()


@pytest.mark.asyncio
async def test_validate_artwork_exists():
    service = ArtInstituteService()
    try:
        exists = await service.validate_artwork_exists(27992)
        assert exists is True
        
        not_exists = await service.validate_artwork_exists(999999999)
        assert not_exists is False
    finally:
        await service.close()
