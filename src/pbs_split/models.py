import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Self, TypedDict

from pbs_split.snippets.hash.model import HashedFile, HashedFileProtocol, HashedFileTD
from pbs_split.snippets.indexed_string.model import (
    IndexedString,
    IndexedStringProtocol,
    IndexedStringTD,
)
from pbs_split.snippets.validate_file_out import validate_file_out


class PageTD(TypedDict):
    package_hash: HashedFileTD
    page_index: int
    lines: List[IndexedStringTD]


class TripTD(TypedDict):
    package_hash: HashedFileTD
    page_hash: HashedFileTD
    trip_index: int
    lines: List[IndexedStringTD]


@dataclass
class Page:
    package_hash: HashedFileProtocol
    page_index: int
    lines: List[IndexedStringProtocol] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: PageTD) -> Self:
        return cls(
            package_hash=HashedFile(**data.get("package_hash")),
            page_index=data.get("page_index"),
            lines=[IndexedString(**x) for x in data.get("lines")],
        )

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))


@dataclass
class Trip:
    package_hash: HashedFileProtocol
    page_hash: HashedFileProtocol
    trip_index: int
    lines: List[IndexedStringProtocol] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: TripTD) -> Self:
        return cls(
            package_hash=HashedFile(**data.get("package_hash")),
            page_hash=HashedFile(**data.get("page_hash")),
            trip_index=data.get("trip_index"),
            lines=[IndexedString(**x) for x in data.get("lines")],
        )

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        input_string = file_path.read_text(encoding="utf-8")
        input_dict = json.loads(input_string)
        return cls.from_dict(input_dict)

    def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
        validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
        path_out.write_text(json.dumps(asdict(self), indent=indent))
