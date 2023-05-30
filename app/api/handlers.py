import uuid

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.car import get_car_after_update
from app.actions.cargo import (create_new_cargo, delete_cargo_from_db,
                               get_cargo_after_update,
                               get_cargo_with_cars_numbers,
                               get_cargos_with_count_cars)
from app.api.filters import CargoFilter
from app.api.schemas import (CreateCargo, GetCar, GetCargo,
                             GetCargoWithCarsNumbers, GetCargoWithCountCars,
                             UpdateCar, UpdateCargo)
from app.db.session import get_db
from settings import MAX_DISTANCE_TO_CARGO

router = APIRouter()


@router.post(
    "/cargo/",
    response_model=GetCargo,
    status_code=201
)
async def create_cargo(
    body: CreateCargo,
    session: AsyncSession = Depends(get_db),
):
    """
    Создание груза
    """

    cargo = await create_new_cargo(body=body, session=session)
    return GetCargo.from_orm(cargo)


@router.get(
    "/cargos/",
    response_model=list[GetCargoWithCountCars],
)
async def get_cargos(
    max_car_distance: int | None = MAX_DISTANCE_TO_CARGO,
    session: AsyncSession = Depends(get_db),
    cargos_filter: CargoFilter = FilterDepends(CargoFilter),
):
    """
    Получение списка грузов
    """

    cargos = await get_cargos_with_count_cars(
        session=session,
        cargos_filter=cargos_filter,
        max_distance_to_cargo=max_car_distance
    )

    cargo_list = [GetCargoWithCountCars.from_orm(cargo) for cargo in cargos]

    return cargo_list


@router.get(
    "/cargo/{id}",
    response_model=GetCargoWithCarsNumbers
)
async def get_cargo(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    """
    Получение груза по id
    """

    cargo = await get_cargo_with_cars_numbers(id=id, session=session)

    return GetCargoWithCarsNumbers.from_orm(cargo)


@router.patch(
    "/car/{id}",
    response_model=GetCar
)
async def update_car(
    id: str,
    body: UpdateCar,
    session: AsyncSession = Depends(get_db),
):
    """
    Изменение авто по id
    """

    car = await get_car_after_update(id=id, body=body, session=session)

    return GetCar.from_orm(car)


@router.patch(
    "/cargo/{id}",
    response_model=GetCargo
)
async def update_cargo(
    id: uuid.UUID,
    body: UpdateCargo,
    session: AsyncSession = Depends(get_db),
):
    """
    Изменение груза по id
    """

    cargo = await get_cargo_after_update(id=id, body=body, session=session)
    return GetCargo.from_orm(cargo)


@router.delete(
    "/cargo/{id}",
    status_code=204,
)
async def delete_cargo(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    """
    Удаление груза по id
    """

    await delete_cargo_from_db(id=id, session=session)

    return None
