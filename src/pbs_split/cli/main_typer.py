"""Command-line interface."""

from time import perf_counter_ns
from typing import Annotated

import typer


def default_options(
    ctx: typer.Context,
    debug: Annotated[bool, typer.Option(help="Enable debug output.")] = False,
    verbosity: Annotated[int, typer.Option("-v", help="Verbosity.", count=True)] = 1,
):
    """"""

    ctx.ensure_object(dict)
    ctx.obj["START_TIME"] = perf_counter_ns()
    ctx.obj["DEBUG"] = debug
    typer.echo(f"Verbosity: {verbosity}")
    ctx.obj["VERBOSITY"] = verbosity


app = typer.Typer(callback=default_options)


@app.command()
def hello(
    ctx: typer.Context, name: Annotated[str, typer.Argument(help="name to greet.")]
):

    typer.echo(f"Hello  {name}!")


if __name__ == "__main__":
    app()
