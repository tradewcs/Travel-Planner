from uuid import UUID
from typing import Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from app.api.dependencies import get_project_service
from app.services.project_service import ProjectService
from app.schemas import (
    ProjectInDB,
    ProjectCreate,
    ProjectUpdate,
    PaginatedResponse,
)
from app.db import (
    ProjectStatus
)
from app.schemas.api_responses import APIResponse
from app.core.exceptions import ResourceNotFound, BusinessRuleViolation


router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=APIResponse[ProjectInDB])
async def create_project(
    project_data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Create a new travel project."""
    try:
        project = await project_service.create_project(
            name=project_data.name,
            description=project_data.description,
            start_date=project_data.start_date,
            place_ids=project_data.place_ids
        )
        return APIResponse(data=ProjectInDB.model_validate(project))
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=PaginatedResponse[ProjectInDB])
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[ProjectStatus] = None,
    project_service: ProjectService = Depends(get_project_service)
):
    """List all travel projects with pagination."""
    projects = await project_service.list_projects(
        skip=skip, limit=limit, status=status
    )
    total = len(projects)  # In real app, get total count from repo

    return PaginatedResponse(
        data=[ProjectInDB.model_validate(p) for p in projects],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{project_id}", response_model=APIResponse[ProjectInDB])
async def get_project(
    project_id: UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    """Get a specific project by ID."""
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return APIResponse(data=ProjectInDB.model_validate(project))


@router.put("/{project_id}", response_model=APIResponse[ProjectInDB])
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Update project information."""
    try:
        project = await project_service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description,
            start_date=project_data.start_date
        )
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return APIResponse(data=ProjectInDB.model_validate(project))
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    """Delete a project (only if no places are visited)."""
    try:
        deleted = await project_service.delete_project(project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Project not found")
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))
