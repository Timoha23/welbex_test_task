import asyncio
import random
import string

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Car, Location
from app.db.session import async_session


class MaxCarsError(Exception):
    pass


class CarCreater:
    """
    Класс для созданя и получения номеров авто
    """

    car_numbers = []

    cars_in_the_fleet = 0
    max_cars = 20

    def __new__(cls, *args, **kwargs) -> None:
        if cls.cars_in_the_fleet == cls.max_cars:
            raise MaxCarsError("В автопарке нет мест.")
        instance = super().__new__(cls)
        cls.cars_in_the_fleet += 1
        return instance

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.car_number = None
        self.location = None
        self.loading_capacity = None

    def _get_random_car_number(self) -> str:
        """
        Генерируем случайный номер автомобиля
        """

        min_digit, max_digit = 1000, 9999

        random_number = random.randint(min_digit, max_digit)
        random_letter = random.choice(string.ascii_uppercase)
        full_number = str(random_number) + random_letter
        return full_number

    def _set_car_number(self) -> None:
        """
        Устанавливаем номер авто
        """

        car_number = self._get_random_car_number()
        it_used = self._check_car_number(car_number)
        while it_used:
            car_number = self._get_random_car_number()
            it_used = self._check_car_number(car_number)
        self._add_car_number(car_number)
        self.car_number = car_number

    def _set_random_loading_capacity(self) -> None:
        """
        Устанавливаем случайную грузоподъемность
        """

        self.loading_capacity = random.randint(1, 1000)

    async def _set_random_location(self) -> None:
        """
        Устанавливаем рандомную локацию
        """
        async with self.session.begin():
            query = select(Location).order_by(func.random()).limit(1)
            res = await self.session.execute(query)
            self.location = res.fetchone()[0]

    @classmethod
    def _check_car_number(cls, car_number) -> bool:
        return car_number in cls.car_numbers

    @classmethod
    def _add_car_number(cls, car_number) -> None:
        cls.car_numbers.append(car_number)

    async def __call__(self):
        self._set_car_number()
        self._set_random_loading_capacity()
        await self._set_random_location()
        return self


async def main():
    session: AsyncSession = async_session()

    async with session.begin():
        query = select(Car)
        res = await session.execute(query)
        length_res = len(res.fetchall())

    if length_res < 1:
        while True:
            try:
                car = await CarCreater(session)()
                async with session.begin():
                    car_db = Car(
                        id=car.car_number,
                        location_zip_code=car.location.zip_code,
                        load_capacity=car.loading_capacity,
                    )
                    session.add(car_db)
            except MaxCarsError:
                break

if __name__ == "__main__":
    asyncio.run(main())
