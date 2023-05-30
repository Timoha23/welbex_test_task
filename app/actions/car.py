from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UpdateCar
from app.db.models import Car, Location


async def get_car_after_update(
        id: str,
        body: UpdateCar,
        session: AsyncSession
) -> Car | HTTPException:
    """
    Обновление и возвращение объекта Car
    """

    async with session.begin():
        location_query = (select(Location)
                          .where(Location.zip_code == body.zip_code))
        location = await session.scalar(location_query)
        if location is None:
            raise HTTPException(
                status_code=404,
                detail=f"Локация с zip_code {body.zip_code} не найдена"
            )
        car_query = select(Car).where(Car.id == id)
        car = await session.scalar(car_query)
        if car is None:
            raise HTTPException(
                status_code=404,
                detail=f"Автомобиль с номером {id} не найден"
            )
        car.location = location
        return car
