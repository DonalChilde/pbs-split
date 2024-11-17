from pathlib import Path
from typing import Iterable, Iterator, List
from uuid import uuid4

from pfmsoft.snippets.indexed_string.index_strings import index_lines_in_file
from pfmsoft.snippets.indexed_string.model import IndexedString

from pbs_split.models import PageLines, page_lines_serializer


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


def parse_pages_from_file(path_in: Path) -> Iterator[PageLines]:
    reader = index_lines_in_file(file_path=path_in, index_start=1)
    yield from parse_pages(lines=reader)


def parse_pages(lines: Iterator[IndexedString]) -> Iterator[PageLines]:
    for idx, lines_of_page in enumerate(package_to_lines_of_pages(lines), start=1):
        page = PageLines(uuid=str(uuid4()), idx=idx, lines=lines_of_page)
        yield page


def write_pages(
    file_stem: str, pages: Iterator[PageLines], path_out: Path, overwrite: bool
) -> int:
    pages_list = list(pages)
    count = 0
    for idx, page in enumerate(pages_list, start=1):
        result_path = path_out / Path(
            f"{file_stem}.page_{idx}_of_{len(pages_list)}.json"
        )
        serializer = page_lines_serializer()
        serializer.save_as_json(
            path_out=result_path, complex_obj=page, overwrite=overwrite
        )
        count = idx
    return count
