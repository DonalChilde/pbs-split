from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter_ns
from typing import Iterable, List

import typer
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TotalFileSizeColumn,
)
from typing_extensions import Annotated

from pbs_split.extract_trips import write_trips
from pbs_split.snippets.file.path_delta import path_delta

app = typer.Typer()


@app.command()
def trips(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Text file with pages, or a directory containing the text files.",
            exists=True,
            file_okay=True,
            dir_okay=True,
        ),
    ],
    path_out: Annotated[
        Path,
        typer.Argument(help="The output directory."),
    ],
    create_subdir: Annotated[
        bool,
        typer.Option(help="Create a subdirectory for the output of each input file."),
    ] = True,
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    extract_trips(
        ctx=ctx,
        path_in=path_in,
        path_out=path_out,
        create_subdir=create_subdir,
        overwrite=overwrite,
    )


def extract_trips(
    ctx: typer.Context,
    path_in: Path,
    path_out: Path,
    create_subdir: bool = True,
    overwrite: bool = False,
):
    input_paths: List[Path] = []
    if path_in.is_dir():
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob("*-page_*") if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        input_paths.extend(files)
    elif path_in.is_file():
        input_paths.append(path_in)
    else:
        raise typer.BadParameter(
            "Input path is not a valid file, or directory containing valid files.\n"
            "Files are expected to match *-page_*"
        )
    typer.echo(f"Searching {len(input_paths)} files for trips.")
    total_trips = 0
    dest_dir: Path = Path("")
    for source_path in input_paths:
        if create_subdir:
            dest_dir = path_out / Path("trips")
        else:
            dest_dir = path_out
        trip_count = write_trips(source_path, dest_dir, overwrite)
        total_trips += trip_count
    typer.echo(
        f"Found {total_trips} trips in {len(input_paths)} files, output to {dest_dir}"
    )
