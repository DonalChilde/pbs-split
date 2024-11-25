"""Typer cli to split pbs package txt to pages."""

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

from pbs_split.extract_pages import parse_pages_from_file, write_pages

logger = logging.getLogger(__name__)
app = typer.Typer()


@dataclass
class SplitPageJob:
    """Job container."""

    path_in: Path
    path_out: Path
    overwrite: bool = False


def total_size_of_files(jobs: Sequence[SplitPageJob]) -> int:
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
    """Split the text version of a PBS pairing package into pages."""
    _ = ctx
    jobs = collect_jobs(path_in=path_in, path_out=path_out, overwrite=overwrite)
    extract_pages_rich(jobs=jobs)


def collect_jobs(
    path_in: Path, path_out: Path, overwrite: bool
) -> Sequence[SplitPageJob]:
    """Build a collections of jobs to do."""
    if path_in.is_dir():
        files = [f for f in path_in.glob(".txt", case_sensitive=False) if f.is_file()]
    elif path_in.is_file():
        files = [path_in]
    else:
        raise typer.BadParameter(
            "Input path is not a valid file, or directory containing valid files."
        )
    jobs: list[SplitPageJob] = []
    for file in files:
        if len(files) > 1:
            dest_dir = path_out / Path(file.stem) / Path("pages")
        else:
            dest_dir = path_out
        jobs.append(SplitPageJob(path_in=file, path_out=dest_dir, overwrite=overwrite))
    return jobs


def extract_pages_rich(jobs: Sequence[SplitPageJob]):
    """Process the jobs to split pages."""
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
        total_pages = 0
        for idx, job in enumerate(jobs, start=1):
            pages = parse_pages_from_file(path_in=job.path_in)
            page_count = write_pages(
                file_stem=job.path_in.stem,
                pages=pages,
                path_out=job.path_out,
                overwrite=job.overwrite,
            )
            total_pages += page_count
            progress.update(
                task,
                advance=job.path_in.stat().st_size,
                description=f"{idx} of {file_count}, {total_pages} pages found.",
            )
