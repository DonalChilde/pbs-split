from pathlib import Path
from typing import Iterator


def line_number_reader(
    file_path: Path,
    index_start=1,
) -> Iterator[tuple[int, str]]:
    """yield enumerated lines in a text file."""
    with open(file_path, encoding="utf-8") as file:
        for idx, line in enumerate(file, start=index_start):
            yield (idx, line)
