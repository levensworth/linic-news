import typing

from src.misc.casing_utils import CamelCaseDTO

T = typing.TypeVar("T")

V = typing.TypeVar("V")


class Page(CamelCaseDTO, typing.Generic[T]):
    data: list[T]
    pagination: "PaginationMetadata"

    @staticmethod
    def of(
        data: list[V],
        total_count: int,
        offset: int | None = None,
        page_size: int | None = None,
    ) -> "Page[V]":
        return Page(
            data=data,
            pagination=PaginationMetadata(
                total_count=total_count,
                page_size=page_size or len(data),
                offset=offset or 0,
            ),
        )

    @staticmethod
    def empty(type: typing.Type[V]) -> "Page[V]":
        data: list[type] = []
        return Page.of(data=data, total_count=0)

    def is_empty(self) -> bool:
        return len(self.data) == 0


class PaginationMetadata(CamelCaseDTO):
    total_count: int
    page_size: int
    offset: int = 0


Page.model_rebuild()