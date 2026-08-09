from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Reservation, Resource, User
from app.schemas.reservation import ReservationCreate

def create_reservation(
        db: Session,
        current_user: User,
        reservation_data: ReservationCreate,
) -> Reservation:
    #1. 不能预约过去的时间
    if reservation_data.start_time <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能预约过去的时间"
        )
    #2. 查询资源是否存在
    resource = db.get(
        Resource,
        reservation_data.resource_id,
    )
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="资源不存在",
        )
    #3. MVP 暂时只允许同一天内的预约
    if (
        reservation_data.start_time.date() !=
        reservation_data.end_time.date()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="暂时只允许同一天内的预约",
        )
    #4. 查询资源是否在开放时间内
    requested_start = reservation_data.start_time.time()
    requested_end = reservation_data.end_time.time()
    if (
        requested_start < resource.open_time or
        requested_end > resource.close_time
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"预约时间不在资源开放时间内",
                f"({resource.open_time} - {resource.close_time})"
            ),
        )

    #5. 检查是否与有效预约冲突
    conflict_statement = (
        select(Reservation)
        .where(
            Reservation.resource_id == reservation_data.resource_id,
            Reservation.status == "created",
            Reservation.start_time < reservation_data.end_time,
            Reservation.end_time > reservation_data.start_time,
        )
        .limit(1)
    )

    conflict_reservation = db.scalar(conflict_statement)

    if conflict_reservation is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该资源在所选时间段已被预约",
        )

    #6. 创建预约对象
    reservation = Reservation(
        user_id = current_user.id,
        resource_id = reservation_data.resource_id,
        start_time = reservation_data.start_time,
        end_time = reservation_data.end_time,
        status = "created",
    )
    try:
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation
    except Exception:
        db.rollback()
        raise

def get_my_reservations(
        db: Session,
        current_user: User,
) -> list[Reservation]:
    statement =(
        select(Reservation)
        .where(
            Reservation.user_id == current_user.id,
        )
        .order_by(
            Reservation.start_time.desc()
        )
    )
    return list(
        db.scalars(statement).all()
    )

def cancel_reservation(
        db: Session,
        current_user: User,
        reservation_id: int,
) -> Reservation:
    statement = select(Reservation).where(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id,
    )
    reservation = db.scalar(statement)
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="预约不存在",
        )
    # 已取消时直接返回，避免重复修改
    if reservation.status == "cancelled":
        return reservation
    reservation.status = "cancelled"
    try:
        db.commit()
        db.refresh(reservation)
        return reservation
    except Exception:
        db.rollback()
        raise