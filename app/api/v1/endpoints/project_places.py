from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_project_service
from app.services.project_service import ProjectService
from app.schemas.project_place import (
    ProjectPlaceCreate,
    ProjectPlaceUpdate,
    ProjectPlaceWithPlace,
)
from app.schemas.api_responses import APIResponse
from app.core.exceptions import ResourceNotFound, BusinessRuleViolation

router = APIRouter(prefix="/projects/{project_id}/places", tags=["project-places"])


@router.post("/", response_model=APIResponse[ProjectPlaceWithPlace])
async def add_place_to_project(
    project_id: UUID,
    place_data: ProjectPlaceCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Add a place to a project."""
    try:
        project_place = await project_service.add_place_to_project(
            project_id=project_id,
            artwork_id=place_data.artwork_id
        )

        if place_data.notes and project_place:
            project_place = await project_service.update_place_in_project(
                project_id=project_id,
                place_id=project_place.place_id,
                notes=place_data.notes
            )

        return APIResponse(data=ProjectPlaceWithPlace.model_validate(project_place))
    except ResourceNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=APIResponse[list[ProjectPlaceWithPlace]])
async def list_project_places(
    project_id: UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    """List all places in a project."""
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return APIResponse(
        data=[ProjectPlaceWithPlace.model_validate(pp) for pp in project.project_places]
    )


@router.get("/{place_id}", response_model=APIResponse[ProjectPlaceWithPlace])
async def get_project_place(
    project_id: UUID,
    place_id: UUID,
    project_service: ProjectService = Depends(get_project_service)
):
    """Get a specific place within a project."""
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_place = next(
        (pp for pp in project.project_places if pp.place_id == place_id), 
        None
    )
    if not project_place:
        raise HTTPException(status_code=404, detail="Place not found in project")

    return APIResponse(data=ProjectPlaceWithPlace.model_validate(project_place))


@router.patch("/{place_id}", response_model=APIResponse[ProjectPlaceWithPlace])
async def update_project_place(
    project_id: UUID,
    place_id: UUID,
    update_data: ProjectPlaceUpdate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Update notes or visited status for a place in a project."""
    try:
        project_place = await project_service.update_place_in_project(
            project_id=project_id,
            place_id=place_id,
            notes=update_data.notes,
            visited=update_data.visited
        )
        if not project_place:
            raise HTTPException(status_code=404, detail="Place not found in project")

        return APIResponse(data=ProjectPlaceWithPlace.model_validate(project_place))
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Place not found in project")
