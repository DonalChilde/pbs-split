from pathlib import Path
from typing import TYPE_CHECKING, Callable

from pbs_split.snippets.hash.hash_file import hash_file
from pbs_split.snippets.hash.model import HashedFile, HashedFileProtocol

if TYPE_CHECKING:
    from hashlib import _Hash


def hashed_file_result_factory(
    file_name: str, hash_str: str, hash_method: str
) -> HashedFileProtocol:
    """An example of a result factory."""
    return HashedFile(file_name=file_name, hash_str=hash_str, hash_method=hash_method)


def make_hashed_file(
    file_path: Path,
    hasher: "_Hash",
    block_size: int = 2**10 * 64,
    result_factory: Callable[[str, str, str], HashedFileProtocol] = HashedFile,
):
    hash_str = hash_file(file_path=file_path, hasher=hasher, block_size=block_size)
    return result_factory(file_path.name, hash_str, hasher.name)
