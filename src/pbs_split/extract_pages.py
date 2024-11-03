import json
from pathlib import Path
from typing import Iterable, Iterator, List

from pbs_split.indexed_line_reader import indexed_line_reader
from pbs_split.snippets.validate_file_out import validate_file_out


def pages_to_lines(
    lines: Iterable[tuple[int, str]]
) -> Iterator[Iterable[tuple[int, str]]]:
    accumulated_lines: List[tuple[int, str]] = []
    first_page = -1
    lines_in_current_page = 0
    lines_since_last_page = 0
    is_page = False
    for indexed_line in lines:
        if is_page:
            accumulated_lines.append(indexed_line)
        else:
            if "DEPARTURE" in indexed_line[1]:
                is_page = True
                if first_page == -1:
                    first_page = indexed_line[0]
            else:
                lines_since_last_page += 1

        if "COCKPIT" in indexed_line[1]:
            result = tuple(accumulated_lines)
            accumulated_lines = []
            is_page = False
            lines_since_last_page = 0
            yield result
    end_result = [
        (-1, "END_RESULT"),
        (first_page, "Line number of first page detected"),
        (lines_since_last_page, "Lines since the end of the last page"),
    ]
    end_result.extend(accumulated_lines)
    yield tuple(end_result)


def write_pages(path_in: Path, path_out: Path, overwrite: bool) -> int:
    reader = indexed_line_reader(path_in)
    count = 0
    for idx, page in enumerate(pages_to_lines(reader), start=1):
        result = {
            "source": path_in.name,
            "page_index": idx,
            "lines": page,
        }
        result_path = path_out / Path(f"{path_in.name}-page_{idx}.json")
        validate_file_out(result_path, overwrite=overwrite, ensure_parent=True)
        result_path.write_text(json.dumps(result, indent=1))
        count = idx
    return count
