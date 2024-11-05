"""Command-line interface."""

from pathlib import Path
from time import perf_counter_ns
from typing import Annotated, List

import typer

from pbs_split.extract_pages import write_pages
from pbs_split.extract_trips import write_trips
from pbs_split.snippets.task_complete_typer import task_complete


def default_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """"""

    ctx.ensure_object(dict)
    ctx.obj["START_TIME"] = perf_counter_ns()
    ctx.obj["DEBUG"] = debug
    ctx.obj["VERBOSITY"] = verbosity
    if ctx.obj["VERBOSITY"] > 1:
        typer.echo(f"Verbosity: {verbosity}")
        typer.echo(f"Debug: {ctx.obj["DEBUG"]}")


app = typer.Typer(callback=default_options)


@app.command()
def pages(
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
    task_complete(ctx=ctx)


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
        page_count = write_pages(source_path, dest_dir, overwrite)
        typer.echo(
            f"Found {page_count} pages in {source_path.name}, output to {dest_dir}"
        )


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
    task_complete(ctx=ctx)


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


@app.command()
def text(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="Pdf file, or a directory containing the Pdf files.",
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
    # call pdf2txt from here.
    task_complete(ctx=ctx)


def extract_text():
    pass


if __name__ == "__main__":
    app()

# maybe have two groups, basic commands, and multi commands? extract-all, pages-all, trips-all, do-all?
# the all commands enforce data directory layout?
