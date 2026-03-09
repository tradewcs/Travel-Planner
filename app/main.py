from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1.routers.api_router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.
    """
    print("Starting Travel Planner API...")
    await init_db()
    print("Database initialized")
    yield
    print("Shutting down...")
    await close_db()
    print("Goodbye!")


def create_application() -> FastAPI:
    """
    Application factory.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="Travel Planner API with Art Institute of Chicago integration",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["health"])
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": "1.0.0"
        }

    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "Welcome to Travel Planner API",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "version": "1.0.0"
        }

    return app


app = create_application()


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
