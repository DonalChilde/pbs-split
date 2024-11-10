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

from pbs_split.extract_pages import parse_pages, write_pages
from pbs_split.snippets.file.path_delta import path_delta

app = typer.Typer()


@dataclass
class SplitPageJob:
    path_in: Path
    path_out: Path
    create_subdir: bool = True
    overwrite: bool = False


@dataclass
class SplitPageJobs:
    jobs: List[SplitPageJob] = field(default_factory=list)


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
    create_subdir: Annotated[
        bool,
        typer.Option(help="Create a subdirectory for the output of each input file."),
    ] = True,
    overwrite: Annotated[
        bool,
        typer.Option(help="Allow overwriting output files."),
    ] = False,
):
    """"""
    extract_pages(
        ctx=ctx,
        path_in=path_in,
        path_out=path_out,
        create_subdir=create_subdir,
        overwrite=overwrite,
    )


def split_pages(ctx: typer.Context, jobs: SplitPageJobs):
    pass


def extract_pages(
    ctx: typer.Context,
    path_in: Path,
    path_out: Path,
    create_subdir: bool = True,
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
        if create_subdir:
            dest_dir = path_out / Path(source_path.stem) / Path("pages")
        else:
            dest_dir = path_out
        pages = parse_pages(path_in=source_path)
        write_count = write_pages(
            file_stem=source_path.stem,
            pages=pages,
            path_out=dest_dir,
            overwrite=overwrite,
        )
        typer.echo(
            f"Found {write_count} pages in {source_path.name}, output to {dest_dir}"
        )
