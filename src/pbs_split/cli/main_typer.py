"""Command-line interface."""

from pathlib import Path
from time import perf_counter_ns
from typing import Annotated, List

import typer

from pbs_split.cli import pages_cli, trips_cli
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
app.add_typer(pages_cli.app, name="pages")
app.add_typer(trips_cli.app, name="trips")


if __name__ == "__main__":
    app()
