from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field

from app.db.models import Cargo


class CargoFilter(Filter):
    weight__lte: int | None = Field(le=1000, ge=1)
    weight__gte: int | None = Field(le=1000, ge=1)

    class Constants(Filter.Constants):
        model = Cargo
