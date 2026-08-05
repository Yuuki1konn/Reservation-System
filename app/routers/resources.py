from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models import Resource, User
from app.schemas.resource import ResourceCreate, ResourceResponse
from app.services.resource_service import (
    create_resource,
    get_resource_by_id,
    get_resource,
)
router = APIRouter(
    prefix="/resources",
    tags=["资源"],
)

@router.post(
    "",
    response_model=ResourceResponse,
    status_code = status.HTTP_201_CREATED,
)
def create_resource_endpoint(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Resource:
    return create_resource(
        db, 
        resource_data,
    )

@router.get(
    "",
    response_model=list[ResourceResponse],
)
def list_resources(
    db: Session = Depends(get_db),
) -> list[Resource]:
    return get_resource(db)

@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
)
def read_resource(
    resource_id: int,
    db: Session = Depends(get_db),
) -> Resource:
    resource = get_resource_by_id(
        db,
        resource_id,
    )
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="资源不存在",
        )
    return resource