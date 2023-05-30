import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Cargo(Base):
    """
    Модель груза
    """

    __tablename__ = "cargo"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    pick_up_zip_code: Mapped[str] = mapped_column(
        ForeignKey("location.zip_code", ondelete="CASCADE")
    )
    delivery_zip_code: Mapped[str] = mapped_column(
        ForeignKey("location.zip_code", ondelete="CASCADE")
    )
    weight: Mapped[int]
    description: Mapped[str | None]
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )
    pick_up = relationship(
        "Location",
        backref="cargo_pick_up",
        foreign_keys=[pick_up_zip_code],
        lazy="joined"
    )
    delivery = relationship(
        "Location",
        backref="cargo_delivery",
        foreign_keys=[delivery_zip_code],
        lazy="joined"
    )


class Car(Base):
    """
    Модель автомобиля
    """

    __tablename__ = "car"

    id: Mapped[str] = mapped_column(primary_key=True)
    location_zip_code: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("location.zip_code")
    )
    load_capacity: Mapped[int]
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )

    location = relationship(
        "Location",
        backref="car",
        foreign_keys=[location_zip_code],
        lazy="joined"
    )


class Location(Base):
    """
    Модель локации
    """

    __tablename__ = "location"

    zip_code: Mapped[str] = mapped_column(primary_key=True, unique=True)
    city: Mapped[str]
    state: Mapped[str]
    longitude: Mapped[float]
    latitude: Mapped[float]
    created_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )
