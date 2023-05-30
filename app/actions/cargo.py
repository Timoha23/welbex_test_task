import uuid

from fastapi import HTTPException
from geopy import distance
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.filters import CargoFilter
from app.api.schemas import CreateCargo, UpdateCargo
from app.db.models import Car, Cargo, Location


async def create_new_cargo(
        body: CreateCargo,
        session: AsyncSession
) -> Cargo | HTTPException:
    """
    Создание груза
    """

    async with session.begin():
        pick_up_query = (select(Location)
                         .where(Location.zip_code == body.pick_up))
        delivery_query = (select(Location)
                          .where(Location.zip_code == body.delivery))
        delivery = await session.scalar(delivery_query)
        pick_up = await session.scalar(pick_up_query)
        if delivery is None:
            raise HTTPException(
                status_code=404,
                detail=f"Почтовый индекс {body.delivery} не найден"
            )
        elif pick_up is None:
            raise HTTPException(
                status_code=404,
                detail=f"Почтовый индекс {body.pick_up} не найден"
            )
        cargo = Cargo(
            weight=body.weight,
            description=body.description,
        )
        cargo.delivery = delivery
        cargo.pick_up = pick_up
        session.add(cargo)
        return cargo


async def get_cargos_with_count_cars(
        session: AsyncSession,
        cargos_filter: CargoFilter,
        max_distance_to_cargo: int | None,
) -> list[Cargo]:
    """
    Получение грузов с количеством авто в радиусе max_distance_to_cargo
    (default=450) миль
    """

    async with session.begin():
        cargos_query = select(Cargo)
        cargos_query = cargos_filter.filter(cargos_query)
        cargos = await session.scalars(cargos_query)

        car_query = select(Car)
        cars_sc = await session.scalars(car_query)
        cars = cars_sc.all()

    cargos_list = []

    for cargo in cargos:
        count_cars = 0
        cargo_coordinates = cargo.pick_up.latitude, cargo.pick_up.longitude
        for car in cars:
            if car.load_capacity < cargo.weight:
                continue
            car_coordinates = car.location.latitude, cargo.pick_up.longitude
            if (distance.distance(cargo_coordinates, car_coordinates).miles <=
               max_distance_to_cargo):
                count_cars += 1
        setattr(cargo, "count_cars", count_cars)
        cargos_list.append(cargo)
    return cargos_list


async def get_cargo_with_cars_numbers(
        id: uuid.UUID,
        session: AsyncSession
) -> Cargo | HTTPException:
    """
    Получение груза из БД с определенным id
    """

    async with session.begin():
        cargo_query = select(Cargo).where(Cargo.id == id)
        cargo = await session.scalar(cargo_query)
        if cargo is None:
            raise HTTPException(
                status_code=404,
                detail=f"Груз с id {id} не найден"
            )
        car_query = select(Car)
        cars = await session.scalars(car_query)

        cargo_coordinates = cargo.pick_up.latitude, cargo.pick_up.longitude

        cars_numbers = []
        for car in cars:
            car = car
            car_coordinates = car.location.latitude, cargo.pick_up.longitude
            car_distance = distance.distance(
                cargo_coordinates, car_coordinates
            ).miles
            cars_numbers.append({"car_number": car.id,
                                 "car_distance": car_distance})
        setattr(cargo, "cars", cars_numbers)
        return cargo


async def get_cargo_after_update(
        id: uuid.UUID,
        body: UpdateCargo,
        session: AsyncSession
) -> Cargo | HTTPException:
    """
    Обновление и возвращение объекта cargo
    """

    async with session.begin():
        query = select(Cargo).where(Cargo.id == id)
        cargo = await session.scalar(query)

        for attr, value in body:
            if value is not None:
                setattr(cargo, attr, value)

        if cargo is None:
            raise HTTPException(
                status_code=404,
                detail=f"Груз с id {id} не найден"
            )
        return cargo


async def delete_cargo_from_db(
        id: uuid.UUID,
        session: AsyncSession
) -> None:
    """
    Удаление груза по id
    """

    async with session.begin():
        query = delete(Cargo).where(Cargo.id == id).returning(Cargo.id)
        cargo_id = await session.scalar(query)
        if cargo_id is None:
            raise HTTPException(
                status_code=404,
                detail=f"Груз с id {id} не найден"
            )
