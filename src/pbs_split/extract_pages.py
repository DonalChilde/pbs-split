import json
from dataclasses import asdict
from hashlib import md5
from pathlib import Path
from typing import Iterable, Iterator, List

from pbs_split.models import Page
from pbs_split.snippets.file.line_number_reader import line_number_reader
from pbs_split.snippets.hash.make_hashed_file import make_hashed_file
from pbs_split.snippets.indexed_string.index_strings import index_file
from pbs_split.snippets.indexed_string.model import IndexedStringProtocol
from pbs_split.snippets.validate_file_out import validate_file_out


def pages_to_lines(
    lines: Iterable[IndexedStringProtocol],
) -> Iterator[List[IndexedStringProtocol]]:
    accumulated_lines: List[IndexedStringProtocol] = []
    first_page = -1
    lines_in_current_page = 0
    lines_since_last_page = 0
    is_page = False
    for indexed_line in lines:
        if is_page:
            accumulated_lines.append(indexed_line)
        else:
            if "DEPARTURE" in indexed_line.txt:
                is_page = True
                accumulated_lines.append(indexed_line)
                if first_page == -1:
                    first_page = indexed_line.idx
            else:
                lines_since_last_page += 1

        if "COCKPIT" in indexed_line.txt:
            result = accumulated_lines
            accumulated_lines = []
            is_page = False
            lines_since_last_page = 0
            yield result


def write_pages(path_in: Path, path_out: Path, overwrite: bool) -> int:
    reader = index_file(file_path=path_in, index_start=1)
    count = 0
    hashed_file = make_hashed_file(path_in, hasher=md5())
    for idx, page_lines in enumerate(pages_to_lines(reader), start=1):
        page = Page(package_hash=hashed_file, page_index=idx, lines=page_lines)
        result_path = path_out / Path(f"{path_in.name}-page_{idx}.json")
        page.to_file(path_out=result_path, overwrite=overwrite)
        count = idx
    return count
