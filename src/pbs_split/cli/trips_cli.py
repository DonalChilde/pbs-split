"""Typer cli to split pages into trips."""

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

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

from pbs_split.extract_trips import parse_trips_from_file, write_trips

logger = logging.getLogger(__name__)
app = typer.Typer()


@dataclass
class SplitTripJob:
    """Job container."""

    path_in: Path
    path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[SplitTripJob]) -> int:
    """Get total file size of jobs."""
    total = 0
    for job in jobs:
        total += job.path_in.stat().st_size
    return total


@app.command()
def split(
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
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """Split a page into trips."""
    _ = ctx
    jobs = collect_jobs(path_in=path_in, path_out=path_out, overwrite=overwrite)
    extract_trips_rich(jobs=jobs)


def collect_jobs(
    path_in: Path, path_out: Path, overwrite: bool
) -> Sequence[SplitTripJob]:
    """Build a collections of jobs to do."""
    if path_in.is_dir():
        typer.echo(f"Looking for files in {path_in}")
        files = [f for f in path_in.glob("*.page_*") if f.is_file()]
        typer.echo(f"Found {len(files)} files")
        # input_paths.extend(files)
    elif path_in.is_file():
        files = [path_in]
    else:
        raise typer.BadParameter(
            "Input path is not a valid file, or directory containing valid files.\n"
            "Files are expected to match *.page_*"
        )
    typer.echo(f"Searching {len(files)} files for trips.")
    jobs: list[SplitTripJob] = []
    for file in files:
        jobs.append(SplitTripJob(path_in=file, path_out=path_out, overwrite=overwrite))
    return jobs


def extract_trips_rich(jobs: Sequence[SplitTripJob]):
    """Process the jobs to split trips."""
    file_count = len(jobs)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            f"1 of {file_count}", total=total_size_of_files(jobs=jobs)
        )
        total_trips = 0
        for idx, job in enumerate(jobs, start=1):
            trips = parse_trips_from_file(path_in=job.path_in)
            trip_count = write_trips(
                file_stem=job.path_in.stem,
                trips=trips,
                path_out=job.path_out,
                overwrite=job.overwrite,
            )
            total_trips += trip_count
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_trips} trips found.",
            )
