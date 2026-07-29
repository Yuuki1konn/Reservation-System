from datetime import datetime, time
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, String, func, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
if TYPE_CHECKING:
    from app.models.reservation import Reservation
class Resource(Base):
    __tablename__ = "resources"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    open_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
    close_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="resource",
    )