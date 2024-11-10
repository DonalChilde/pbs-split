from hashlib import md5
from pathlib import Path
from typing import Iterable, Iterator, List

from pbs_split.models import Page
from pbs_split.snippets.hash.make_hashed_file import make_hashed_file
from pbs_split.snippets.hash.model import HashedFileProtocol
from pbs_split.snippets.indexed_string.index_strings import index_file_line
from pbs_split.snippets.indexed_string.model import IndexedString, IndexedStrings


def package_to_lines_of_pages(
    lines: Iterable[IndexedString],
) -> Iterator[List[IndexedString]]:
    accumulated_lines: List[IndexedString] = []

    is_page = False
    for indexed_line in lines:
        if is_page:
            accumulated_lines.append(indexed_line)
        else:
            if "DEPARTURE" in indexed_line.txt:
                is_page = True
                accumulated_lines.append(indexed_line)

        if "COCKPIT" in indexed_line.txt:
            result = accumulated_lines
            accumulated_lines = []
            is_page = False
            yield result


def parse_pages_from_file(path_in: Path) -> Iterator[Page]:
    reader = index_file_line(file_path=path_in, index_start=1)
    hashed_file = make_hashed_file(path_in, hasher=md5())
    yield from parse_pages(lines=reader, hashed_file=hashed_file)


def parse_pages(
    lines: Iterator[IndexedString], hashed_file: HashedFileProtocol
) -> Iterator[Page]:
    for idx, lines_of_page in enumerate(package_to_lines_of_pages(lines), start=1):
        indexed_lines = IndexedStrings(strings=tuple(lines_of_page))
        page = Page(package_hash=hashed_file, page_index=idx, lines=indexed_lines)
        yield page


def write_pages(
    file_stem: str, pages: Iterator[Page], path_out: Path, overwrite: bool
) -> int:
    pages_list = list(pages)
    count = 0
    for idx, page in enumerate(pages_list, start=1):
        result_path = path_out / Path(
            f"{file_stem}.page_{idx}_of_{len(pages_list)}.json"
        )
        page.to_file(path_out=result_path, overwrite=overwrite)
        count = idx
    return count
