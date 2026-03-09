from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from sqlalchemy import create_engine

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database, create tables."""
    from app.db.models import BaseModel  # Import all models

    async with engine.begin() as conn:
        # Create tables (in production, use Alembic migrations instead)
        await conn.run_sync(BaseModel.metadata.create_all)


async def close_db() -> None:
    """Close database connection."""
    await engine.dispose()


# For Alembic migrations (sync version)
sync_engine = create_engine(
    settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite"),
    echo=True,
)
