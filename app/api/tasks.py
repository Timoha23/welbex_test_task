from rocketry import Rocketry
from sqlalchemy import func, select

from app.db.models import Car, Location
from app.db.session import async_session
from settings import AUTO_LOCATION_REFRESH_RATE

rocketry = Rocketry(execution="async")


@rocketry.task(f'every {AUTO_LOCATION_REFRESH_RATE} seconds')
async def update_cars_locations():
    session = async_session()
    async with session.begin():
        cars_query = select(Car)
        cars_sc = await session.scalars(cars_query)
        cars = cars_sc.all()
        count_cars = len(cars)

        locations_query = (
            select(Location).order_by(func.random()).limit(count_cars)
        )

        locations_sc = await session.scalars(locations_query)
        locations = locations_sc.all()

        for i in range(count_cars):
            cars[i].location = locations[i]
