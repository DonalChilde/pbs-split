# import json
# from dataclasses import asdict, dataclass, field
# from pathlib import Path
# from typing import List, Self, TypedDict

# from pbs_split.snippets.hash.model import HashedFile, HashedFileProtocol, HashedFileTD
# from pbs_split.snippets.indexed_string.model import (
#     IndexedString,
#     IndexedStrings,
#     IndexedStringTD,
#     IndexedStringsTD,
# )
# from pbs_split.snippets.validate_file_out import validate_file_out


# class PageTD(TypedDict):
#     package_hash: HashedFileTD
#     page_index: int
#     lines: IndexedStringsTD


# class TripTD(TypedDict):
#     package_hash: HashedFileTD
#     page_hash: HashedFileTD
#     trip_index: int
#     header_1: IndexedStringTD
#     header_2: IndexedStringTD
#     footer: IndexedStringTD
#     lines: IndexedStringsTD


# @dataclass
# class Page:
#     package_hash: HashedFileProtocol
#     page_index: int
#     lines: IndexedStrings

#     @classmethod
#     def from_dict(cls, data: PageTD) -> Self:
#         return cls(
#             package_hash=HashedFile(**data.get("package_hash")),  # type: ignore
#             page_index=data.get("page_index"),  # type: ignore
#             lines=IndexedStrings(strings=tuple((IndexedString(**x) for x in data.get("lines").get("strings")))),  # type: ignore
#         )

#     @classmethod
#     def from_file(cls, file_path: Path) -> Self:
#         input_string = file_path.read_text(encoding="utf-8")
#         input_dict = json.loads(input_string)
#         return cls.from_dict(input_dict)

#     def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
#         validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
#         path_out.write_text(json.dumps(asdict(self), indent=indent))


# @dataclass
# class Trip:
#     package_hash: HashedFileProtocol
#     page_hash: HashedFileProtocol
#     trip_index: int
#     header_1: IndexedString
#     header_2: IndexedString
#     footer: IndexedString
#     lines: IndexedStrings

#     @classmethod
#     def from_dict(cls, data: TripTD) -> Self:
#         return cls(
#             package_hash=HashedFile(**data.get("package_hash")),  # type: ignore
#             page_hash=HashedFile(**data.get("page_hash")),  # type: ignore
#             trip_index=data.get("trip_index"),  # type: ignore
#             header_1=IndexedString(**data.get("header_1")),  # type: ignore
#             header_2=IndexedString(**data.get("header_2")),  # type: ignore
#             footer=IndexedString(**data.get("footer")),  # type: ignore
#             lines=IndexedStrings(strings=tuple((IndexedString(**x) for x in data.get("lines").get("strings")))),  # type: ignore
#         )

#     @classmethod
#     def from_file(cls, file_path: Path) -> Self:
#         input_string = file_path.read_text(encoding="utf-8")
#         input_dict = json.loads(input_string)
#         return cls.from_dict(input_dict)

#     def to_file(self, path_out: Path, overwrite: bool, indent: int = 1):
#         validate_file_out(path_out, overwrite=overwrite, ensure_parent=True)
#         path_out.write_text(json.dumps(asdict(self), indent=indent))
