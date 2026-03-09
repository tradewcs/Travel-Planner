from uuid import UUID
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from app.db.models.base import BaseModel


class BaseRepository[ModelT: BaseModel](SQLAlchemyAsyncRepository[ModelT]):
    """Base repository with common functionality."""

    async def get_by_id(self, item_id: UUID) -> ModelT | None:
        """Get an item by ID."""
        return await self.get(item_id)

    async def exists(self, **filters) -> bool:
        """Check if an item exists with given filters."""
        result = await self.count(**filters)
        return result > 0
