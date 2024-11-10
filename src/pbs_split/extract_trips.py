from hashlib import md5
from pathlib import Path
from typing import Iterable, Iterator, List

from pbs_split.models import Page, Trip
from pbs_split.snippets.hash.make_hashed_file import make_hashed_file
from pbs_split.snippets.hash.model import HashedFileProtocol
from pbs_split.snippets.indexed_string.model import IndexedStringProtocol


def page_to_lines_of_trips(
    lines: Iterable[IndexedStringProtocol],
) -> Iterator[List[IndexedStringProtocol]]:
    is_trip = False
    accumulated_lines: List[IndexedStringProtocol] = []
    for indexed_line in lines:
        if is_trip:
            accumulated_lines.append(indexed_line)
        else:
            if indexed_line.txt.startswith("SEQ"):
                is_trip = True
                accumulated_lines.append(indexed_line)
        if indexed_line.txt.startswith("TTL"):
            result = accumulated_lines
            accumulated_lines = []
            is_trip = False
            yield result


def parse_trips(page: Page, page_hash: HashedFileProtocol) -> Iterator[Trip]:
    for idx, trip_lines in enumerate(page_to_lines_of_trips(page.lines), start=1):
        trip = Trip(
            package_hash=page.package_hash,
            page_hash=page_hash,
            trip_index=idx,
            header_1=page.lines[0],
            header_2=page.lines[1],
            footer=page.lines[-1],
            lines=trip_lines,
        )
        yield trip


def write_trips(path_in: Path, path_out: Path, overwrite: bool) -> int:
    page = Page.from_file(path_in)
    hashed_file = make_hashed_file(path_in, hasher=md5())
    count = 0
    for idx, trip in enumerate(parse_trips(page=page, page_hash=hashed_file), start=1):
        result_path = path_out / Path(f"{path_in.stem}-trip_{trip.trip_index}.json")
        trip.to_file(path_out=result_path, overwrite=overwrite)
        count = idx
    return count
