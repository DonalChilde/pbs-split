from dataclasses import dataclass, field
from typing import Protocol, Tuple, TypedDict


@dataclass(slots=True, frozen=True)
class IndexedString:
    idx: int
    txt: str

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}(idx={self.idx}, txt={self.txt!r})"

    def __str__(self):
        return f"{self.idx}: {self.txt!r}"


@dataclass(slots=True, frozen=True)
class IndexedStrings:
    strings: Tuple[IndexedString, ...] = ()


class IndexedStringProtocol(Protocol):
    idx: int
    txt: str


class IndexedStringTD(TypedDict):
    idx: int
    txt: str
