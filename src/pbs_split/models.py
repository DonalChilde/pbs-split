from dataclasses import dataclass, field
from typing import TypedDict

from pfmsoft.snippets.indexed_string.model import IndexedString, IndexedStringTD
from pfmsoft.snippets.simple_serializer import DataclassSerializer


class PageLinesTD(TypedDict):
    uuid: str
    idx: int
    lines: list[IndexedStringTD]


class TripLinesTD(TypedDict):
    uuid: str
    source: str
    idx: int
    lines: list[IndexedStringTD]


@dataclass(slots=True)
class PageLines:
    uuid: str
    idx: int
    lines: list[IndexedString] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: PageLinesTD) -> "PageLines":
        result = PageLines(
            uuid=simple_obj["uuid"],
            idx=simple_obj["idx"],
            lines=[IndexedString(**x) for x in simple_obj["lines"]],
        )
        return result


@dataclass(slots=True)
class TripLines:
    uuid: str
    source: str
    idx: int
    lines: list[IndexedString] = field(default_factory=list)

    @staticmethod
    def from_simple(simple_obj: TripLinesTD) -> "TripLines":
        result = TripLines(
            uuid=simple_obj["uuid"],
            source=simple_obj["source"],
            idx=simple_obj["idx"],
            lines=[IndexedString(**x) for x in simple_obj["lines"]],
        )
        return result


def page_lines_serializer() -> DataclassSerializer[PageLines, PageLinesTD]:
    return DataclassSerializer[PageLines, PageLinesTD](
        complex_factory=PageLines.from_simple
    )


def trip_lines_serializer() -> DataclassSerializer[TripLines, TripLinesTD]:
    return DataclassSerializer[TripLines, TripLinesTD](
        complex_factory=TripLines.from_simple
    )
