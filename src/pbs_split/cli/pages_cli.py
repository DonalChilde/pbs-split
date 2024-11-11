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

from pbs_split.extract_pages import parse_pages_from_file, write_pages
from pbs_split.snippets.file.path_delta import path_delta

app = typer.Typer()


@dataclass
class SplitPageJob:
    path_in: Path
    path_out: Path
    overwrite: bool = False


@dataclass
class SplitPageJobs:
    jobs: List[SplitPageJob] = field(default_factory=list)

    def total_size_of_files(self) -> int:
        total = 0
        for job in self.jobs:
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
    """"""

    if path_in.is_dir():
        files = [f for f in path_in.glob(".txt", case_sensitive=False) if f.is_file()]
    elif path_in.is_file():
        files = [path_in]
    else:
        raise typer.BadParameter(
            "Input path is not a valid file, or directory containing valid files."
        )
    jobs = SplitPageJobs()
    for file in files:
        if len(files) > 1:
            dest_dir = path_out / Path(file.stem) / Path("pages")
        else:
            dest_dir = path_out
        jobs.jobs.append(
            SplitPageJob(path_in=file, path_out=dest_dir, overwrite=overwrite)
        )
    extract_pages_rich(jobs=jobs)


def split_all(ctx: typer.Context, jobs: SplitPageJobs):
    pass


def extract_pages_rich(jobs: SplitPageJobs):
    file_count = len(jobs.jobs)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        FileSizeColumn(),
        TotalFileSizeColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(f"1 of {file_count}", total=jobs.total_size_of_files())
        total_pages = 0
        for idx, job in enumerate(jobs.jobs, start=1):
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


def extract_pages(
    ctx: typer.Context,
    path_in: Path,
    path_out: Path,
    overwrite: bool = False,
):
    input_paths: List[Path] = []
    if path_in.is_dir():
        files = [f for f in path_in.glob(".txt", case_sensitive=False) if f.is_file()]
        input_paths.extend(files)
    elif path_in.is_file():
        input_paths.append(path_in)
    else:
        raise typer.BadParameter(
            "Input path is not a valid file, or directory containing valid files."
        )

    for source_path in input_paths:
        if len(input_paths) > 1:
            dest_dir = path_out / Path(source_path.stem) / Path("pages")
        else:
            dest_dir = path_out
        pages = parse_pages_from_file(path_in=source_path)
        write_count = write_pages(
            file_stem=source_path.stem,
            pages=pages,
            path_out=dest_dir,
            overwrite=overwrite,
        )
        typer.echo(
            f"Found {write_count} pages in {source_path.name}, output to {dest_dir}"
        )
