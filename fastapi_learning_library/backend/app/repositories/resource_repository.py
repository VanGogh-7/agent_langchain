from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import LearningResource
from app.schemas.resource import ResourceCreate, ResourceStatus, ResourceUpdate


def list_resources(
    db: Session,
    *,
    owner_id: int,
    q: str | None = None,
    category: str | None = None,
    status: ResourceStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[LearningResource]:
    statement = select(LearningResource).where(LearningResource.owner_id == owner_id)

    if q:
        pattern = f"%{q}%"
        statement = statement.where(
            or_(
                LearningResource.title.ilike(pattern),
                LearningResource.author.ilike(pattern),
                LearningResource.notes.ilike(pattern),
            )
        )
    if category:
        statement = statement.where(LearningResource.category == category)
    if status:
        statement = statement.where(LearningResource.status == status.value)

    statement = (
        statement.order_by(LearningResource.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(statement))


def get_resource_by_id(db: Session, resource_id: int) -> LearningResource | None:
    return db.get(LearningResource, resource_id)


def create_resource(
    db: Session,
    *,
    owner_id: int,
    resource_in: ResourceCreate,
) -> LearningResource:
    resource = LearningResource(
        owner_id=owner_id,
        title=resource_in.title,
        author=resource_in.author,
        category=resource_in.category,
        status=resource_in.status.value,
        rating=resource_in.rating,
        notes=resource_in.notes,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def update_resource(
    db: Session,
    *,
    resource: LearningResource,
    resource_in: ResourceUpdate,
) -> LearningResource:
    update_data = resource_in.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value

    for field, value in update_data.items():
        setattr(resource, field, value)

    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def delete_resource(db: Session, *, resource: LearningResource) -> None:
    db.delete(resource)
    db.commit()
