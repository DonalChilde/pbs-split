from pathlib import Path
from typing import Iterable, Iterator, List

from pbs_split.snippets.indexed_string.model import IndexedString, IndexedStrings


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


def parse_trips_from_file(path_in: Path) -> Iterator[IndexedStrings]:
    page = IndexedStrings.from_file(path_in)
    yield from parse_trips(page=page)


def parse_trips(page: IndexedStrings) -> Iterator[IndexedStrings]:
    for idx, trip_lines in enumerate(page_to_lines_of_trips(page.strings), start=1):
        _ = idx
        trip = IndexedStrings(
            strings=(page.strings[0], page.strings[1], *trip_lines, page.strings[-1])
        )
        yield trip


def write_trips(
    file_stem: str, trips: Iterator[IndexedStrings], path_out: Path, overwrite: bool
):
    trips_list = list(trips)
    count = 0
    for idx, trip in enumerate(trips_list, start=1):
        result_path = path_out / Path(
            f"{file_stem}.trip_{idx}_of_{len(trips_list)}.json"
        )
        trip.to_file(path_out=result_path, overwrite=overwrite)
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
