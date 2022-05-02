from typing import Generic, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic.types import conint

T = TypeVar("T")


class Page(AbstractPage[T], Generic[T]):
    items: Sequence[T]
    page: conint(ge=1)
    size: conint(ge=1)

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> "Page[T]":
        return cls(
            items=items,
            page=params.page,
            size=params.size,
        )
