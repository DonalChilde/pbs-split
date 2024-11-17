from pathlib import Path
from typing import Iterable, Iterator, List
from uuid import uuid4

from pfmsoft.snippets.indexed_string.model import IndexedString

from pbs_split.models import (
    PageLines,
    TripLines,
    page_lines_serializer,
    trip_lines_serializer,
)


def page_to_lines_of_trips(
    lines: Iterable[IndexedString],
) -> Iterator[List[IndexedString]]:
    is_trip = False
    accumulated_lines: List[IndexedString] = []
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


def parse_trips_from_file(path_in: Path) -> Iterator[TripLines]:
    serializer = page_lines_serializer()
    page = serializer.load_from_json(path_in=path_in)
    yield from parse_trips(page=page)


def parse_trips(page: PageLines) -> Iterator[TripLines]:
    for idx, trip_lines in enumerate(page_to_lines_of_trips(page.lines), start=1):
        trip = TripLines(
            uuid=str(uuid4()),
            source=page.uuid,
            idx=idx,
            lines=[page.lines[0], page.lines[1], *trip_lines, page.lines[-1]],
        )
        yield trip


def write_trips(
    file_stem: str, trips: Iterator[TripLines], path_out: Path, overwrite: bool
):
    trips_list = list(trips)
    count = 0
    for idx, trip in enumerate(trips_list, start=1):
        result_path = path_out / Path(
            f"{file_stem}.trip_{idx}_of_{len(trips_list)}.json"
        )
        serializer = trip_lines_serializer()
        serializer.save_as_json(
            path_out=result_path, complex_obj=trip, overwrite=overwrite
        )
        count = idx
    return count


# def write_trips(path_in: Path, path_out: Path, overwrite: bool) -> int:
#     page = Page.from_file(path_in)
#     hashed_file = make_hashed_file(path_in, hasher=md5())
#     count = 0
#     for idx, trip in enumerate(parse_trips(page=page, page_hash=hashed_file), start=1):
#         result_path = path_out / Path(f"{path_in.stem}-trip_{trip.trip_index}.json")
#         trip.to_file(path_out=result_path, overwrite=overwrite)
#         count = idx
#     return count
