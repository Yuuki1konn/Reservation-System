from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models import Reservation, User
from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse,
)
from app.services.reservation_service import (
    create_reservation,
    cancel_reservation,
    get_my_reservations,
)
router = APIRouter(
    prefix="/reservations",
    tags=["预约"],
)

@router.post(
    "",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation_endpoint(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Reservation:
    return create_reservation(
        db,
        current_user,
        reservation_data,
)

@router.get(
    "/me",
    response_model=list[ReservationResponse],
)
def list_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Reservation]:
    return get_my_reservations(db, current_user,)

@router.post(
    "/{reservation_id}/cancel",
    response_model=ReservationResponse,
)
def cancel_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Reservation:
    return cancel_reservation(
        db,
        current_user,
        reservation_id,
    )