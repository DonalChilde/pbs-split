"""Command-line interface."""

from time import perf_counter_ns
from typing import Annotated

import typer

from pbs_split.cli import pages_cli, trips_cli


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
