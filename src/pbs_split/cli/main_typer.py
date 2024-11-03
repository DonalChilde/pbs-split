"""Command-line interface."""

from pathlib import Path
from time import perf_counter_ns
from typing import Annotated, List

import typer

from pbs_split.extract_pages import write_pages
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
        typer.Argument(help="The output directory.", file_okay=False, writable=True),
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
            dest_dir = path_out / Path(source_path.name)
        else:
            dest_dir = path_out
        page_count = write_pages(source_path, dest_dir, overwrite)
        typer.echo(
            f"Found {page_count} pages in {source_path.name}, output to {dest_dir}"
        )
    task_complete(ctx=ctx)


@app.command()
def trips(ctx: typer.Context):
    task_complete(ctx=ctx)


if __name__ == "__main__":
    app()
