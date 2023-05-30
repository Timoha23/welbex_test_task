import asyncio
import csv
import os
from typing import Generator

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Location
from app.db.session import async_session
from settings import BASE_DIR


def get_locations_objects() -> Generator:
    csv_path = os.path.join(BASE_DIR, "csv")

    csv_locations = os.path.join(csv_path, "uszips.csv")
    with open(csv_locations, "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        locations = []
        limit = 400
        counter = 0
        for row in reader:
            location = {
                "city": row.get("city"),
                "state": row.get("state_name"),
                "zip_code": row.get("zip"),
                "longitude": float(row.get("lng")),
                "latitude": float(row.get("lat")),
            }
            locations.append(location)
            counter += 1
            if counter == limit:
                yield locations
                counter = 0
                locations = []


async def put_data_to_database():
    session: AsyncSession = async_session()
    async with session.begin():
        locations_gen = get_locations_objects()
        for locations in locations_gen:
            query = insert(Location).values(locations).on_conflict_do_nothing()
            await session.execute(query)


async def main():
    task = asyncio.create_task(put_data_to_database())
    await task


if __name__ == "__main__":
    asyncio.run(main())
