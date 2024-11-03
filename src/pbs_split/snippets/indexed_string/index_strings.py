from pathlib import Path
from typing import Callable, Iterable, Iterator

from pbs_split.snippets.indexed_string.model import IndexedString, IndexedStringProtocol


def index_strings(
    strings: Iterable[str],
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    factory: Callable[[int, str], IndexedStringProtocol] = IndexedString,
    index_start=0,
) -> Iterator[IndexedStringProtocol]:
    """
    Enumerate and filter a string iterable, yield matches as an `IndexedStringProtocol`

    Args:
        strings: An iterable of strings.
        string_filter: Used to test strings.
        factory: The factory used to make an indexed string. Defaults to IndexedStringDC.
        index_start: Defaults to 0.

    Yields:
        The matched indexed strings.
    """
    for idx, txt in enumerate(strings, start=index_start):
        indexed_string = factory(idx, txt)
        if string_filter is not None:
            if string_filter(indexed_string):
                yield indexed_string
        yield indexed_string


def index_file(
    file_path: Path,
    string_filter: Callable[[IndexedStringProtocol], bool] | None = None,
    factory: Callable[[int, str], IndexedStringProtocol] = IndexedString,
    index_start=0,
) -> Iterator[IndexedStringProtocol]:
    with open(file_path, encoding="utf-8") as file:
        for idx, line in enumerate(file, start=index_start):
            indexed_string = factory(idx, line)
            if string_filter is not None:
                if string_filter(indexed_string):
                    yield indexed_string
            yield indexed_string
