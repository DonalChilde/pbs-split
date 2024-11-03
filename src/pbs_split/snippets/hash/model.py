from dataclasses import dataclass
from typing import Protocol, TypedDict


class HashedFileProtocol(Protocol):
    file_name: str
    hash_str: str
    hash_method: str


@dataclass(slots=True)
class HashedFile:
    file_name: str
    hash_str: str
    hash_method: str


class HashedFileTD(TypedDict):
    file_name: str
    hash_str: str
    hash_method: str
