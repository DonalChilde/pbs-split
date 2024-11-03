from dataclasses import dataclass
from typing import Protocol, TypedDict


@dataclass(slots=True)
class IndexedString:
    idx: int
    txt: str

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"{cls_name}(idx={self.idx}, txt={self.txt!r})"

    def __str__(self):
        return f"{self.idx}: {self.txt!r}"


class IndexedStringProtocol(Protocol):
    idx: int
    txt: str


class IndexedStringTD(TypedDict):
    idx: int
    txt: str
