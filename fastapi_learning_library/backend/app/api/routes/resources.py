from fastapi import APIRouter, Response, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.resource import (
    ResourceCreate,
    ResourceRead,
    ResourceStatus,
    ResourceUpdate,
)
from app.services import resource_service


router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[ResourceRead])
def list_resources(
    db: DbSession,
    current_user: CurrentUser,
    q: str | None = None,
    category: str | None = None,
    status: ResourceStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ResourceRead]:
    return resource_service.list_user_resources(
        db,
        user=current_user,
        q=q,
        category=category,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource_in: ResourceCreate,
    db: DbSession,
    current_user: CurrentUser,
) -> ResourceRead:
    return resource_service.create_user_resource(
        db,
        user=current_user,
        resource_in=resource_in,
    )


@router.get("/{resource_id}", response_model=ResourceRead)
def get_resource(
    resource_id: int,
    db: DbSession,
    current_user: CurrentUser,
) -> ResourceRead:
    return resource_service.get_user_resource(
        db,
        user=current_user,
        resource_id=resource_id,
    )


@router.put("/{resource_id}", response_model=ResourceRead)
def update_resource(
    resource_id: int,
    resource_in: ResourceUpdate,
    db: DbSession,
    current_user: CurrentUser,
) -> ResourceRead:
    return resource_service.update_user_resource(
        db,
        user=current_user,
        resource_id=resource_id,
        resource_in=resource_in,
    )


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    db: DbSession,
    current_user: CurrentUser,
) -> Response:
    resource_service.delete_user_resource(
        db,
        user=current_user,
        resource_id=resource_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
