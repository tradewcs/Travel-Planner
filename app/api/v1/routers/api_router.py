from fastapi import APIRouter

from app.api.v1.endpoints import projects, project_places, places

api_router = APIRouter()

api_router.include_router(projects.router)
api_router.include_router(project_places.router)
api_router.include_router(places.router)
