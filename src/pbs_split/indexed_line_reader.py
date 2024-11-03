from pathlib import Path
from typing import Iterator


def indexed_line_reader(
    file_path: Path,
    index_start=0,
) -> Iterator[tuple[int, str]]:
    """yield enumerated lines in a text file."""
    with open(file_path, encoding="utf-8") as file:
        for idx, line in enumerate(file, start=index_start):
            yield (idx, line)
