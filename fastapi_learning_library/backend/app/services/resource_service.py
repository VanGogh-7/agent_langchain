from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.db.models import LearningResource, User
from app.repositories import resource_repository
from app.schemas.resource import ResourceCreate, ResourceStatus, ResourceUpdate


def list_user_resources(
    db: Session,
    *,
    user: User,
    q: str | None = None,
    category: str | None = None,
    status: ResourceStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[LearningResource]:
    return resource_repository.list_resources(
        db,
        owner_id=user.id,
        q=q,
        category=category,
        status=status,
        skip=skip,
        limit=limit,
    )


def create_user_resource(
    db: Session,
    *,
    user: User,
    resource_in: ResourceCreate,
) -> LearningResource:
    return resource_repository.create_resource(
        db,
        owner_id=user.id,
        resource_in=resource_in,
    )


def get_user_resource(db: Session, *, user: User, resource_id: int) -> LearningResource:
    resource = resource_repository.get_resource_by_id(db, resource_id)
    if resource is None or resource.owner_id != user.id:
        raise not_found("Resource not found")
    return resource


def update_user_resource(
    db: Session,
    *,
    user: User,
    resource_id: int,
    resource_in: ResourceUpdate,
) -> LearningResource:
    resource = get_user_resource(db, user=user, resource_id=resource_id)
    return resource_repository.update_resource(
        db,
        resource=resource,
        resource_in=resource_in,
    )


def delete_user_resource(db: Session, *, user: User, resource_id: int) -> None:
    resource = get_user_resource(db, user=user, resource_id=resource_id)
    resource_repository.delete_resource(db, resource=resource)
