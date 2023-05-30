import datetime
import uuid

from pydantic import BaseModel, Field


class CreateCargo(BaseModel):
    """
    Создание груза
    """

    pick_up: str
    delivery: str
    weight: int = Field(gt=0, le=1000)
    description: str | None = Field(max_length=512)


class Location(BaseModel):
    zip_code: str
    city: str
    state: str
    longitude: float
    latitude: float
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class GetCargo(BaseModel):
    """
    Получение груза после создания
    """

    id: uuid.UUID
    pick_up: Location
    delivery: Location
    weight: int
    description: str | None
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class GetCargoWithCountCars(GetCargo):
    """
    Получение груза с количество ближайших авто
    """

    count_cars: int

    class Config:
        orm_mode = True


class CarsInfoForOneCargo(BaseModel):
    """
    Вложенная модель для GetCargoWithCarsNumbers
    """

    car_number: str
    car_distance: float


class GetCargoWithCarsNumbers(GetCargo):
    """
    Получение груза с списком номеров ближайших авто
    """

    cars: list[CarsInfoForOneCargo]

    class Config:
        orm_mode = True


class UpdateCar(BaseModel):
    """
    Изменение авто
    """

    zip_code: str


class GetCar(BaseModel):
    """
    Получение инфо о автомобиле
    """

    id: str
    location: Location
    load_capacity: int
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class UpdateCargo(BaseModel):
    """
    Обновление груза
    """

    weight: int | None = Field(gt=0, le=1000)
    description: str | None
