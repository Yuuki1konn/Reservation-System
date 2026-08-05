from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Resource
from app.schemas.resource import ResourceCreate

def create_resource(
        db: Session,
        resource_data: ResourceCreate,
) -> Resource:
    resource = Resource(
        name = resource_data.name.strip(),
        location = resource_data.location.strip(),
        open_time = resource_data.open_time,
        close_time = resource_data.close_time,
    )
    try:
        db.add(resource)
        db.commit()
        db.refresh(resource)
        return resource
    except Exception:
        db.rollback()
        raise

def get_resource(
        db: Session,
) -> list[Resource]:
    statement = select(Resource).order_by(
        Resource.id,
    )
    return list(db.scalars(statement).all())

def get_resource_by_id(
        db: Session,
        resource_id: int,
) -> Resource | None:
    return db.get(Resource, resource_id)