import shutil
import subprocess
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()

# typer ./scripts/split_test_data.py run split-all ~/projects/tmp/pbs-data/2024.11.01-2024.12.01
# typer ./scripts/split_test_data.py run reset ~/projects/tmp/pbs-data/2024.11.01-2024.12.01


def get_text_source_files(path_in: Path) -> list[Path]:
    return list(path_in.glob("*.txt"))


def remove_output_directories(source_file_paths: list[Path]):
    for file_path in source_file_paths:
        parsed_dir = output_base_dir_from_source_file(file_path)
        if parsed_dir.is_dir():
            shutil.rmtree(parsed_dir)


def output_base_dir_from_source_file(source_path: Path) -> Path:
    output_dir = source_path.parent / source_path.stem
    return output_dir


def split_page_dir_from_source_file(source_file: Path) -> Path:
    parsed_dir = output_base_dir_from_source_file(source_file)
    page_dir = parsed_dir / "pages"
    return page_dir


def split_trip_dir_from_source_path(source_file: Path) -> Path:
    parsed_dir = output_base_dir_from_source_file(source_file)
    trip_dir = parsed_dir / "trip"
    return trip_dir


def split_to_pages(source_paths: list[Path]):
    for source_file in source_paths:
        path_out = split_page_dir_from_source_file(source_file)
        path_out.mkdir(parents=True)
        args = [
            "pbs-split",
            "pages",
            "split",
            "--no-overwrite",
            f"{source_file}",
            f"{path_out}",
        ]
        result = subprocess.run(args, capture_output=True, check=True)
        typer.echo(result.stdout)


def split_to_trips(source_paths: list[Path]):
    for source_file in source_paths:
        path_in = split_page_dir_from_source_file(source_file)
        path_out = split_trip_dir_from_source_path(source_file)
        path_out.mkdir(parents=True)
        args = [
            "pbs-split",
            "trips",
            "split",
            "--no-overwrite",
            f"{path_in}",
            f"{path_out}",
        ]
        result = subprocess.run(args, capture_output=True, check=True)
        typer.echo(result.stdout)


@app.command()
def reset(
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing the source files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    """
    Reset the parsed/split data directories.

    Data directories are found in the same directory as the source files, and are named
    based on the Path.stem of the source file.
    """
    source_files = get_text_source_files(path_in=path_in)
    remove_output_directories(source_file_paths=source_files)
    typer.echo(f"Removed parsed directories from {path_in}")


@app.command()
def split_pages(
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing the source files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    """Split pages from source files into the `pages` data directory."""
    source_files = get_text_source_files(path_in=path_in)
    split_to_pages(source_paths=source_files)
    typer.echo(f"Split pages for {len(source_files)} bid packages from {path_in}")


@app.command()
def split_trips(
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing the source files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    """
    Split trips from source files into the `trips` data directory.

    Requires pages to have already been split from source file.
    """
    source_files = get_text_source_files(path_in=path_in)
    split_to_trips(source_paths=source_files)
    typer.echo(f"Split trips for {len(source_files)} bid packages from {path_in}")


@app.command()
def split_all(
    path_in: Annotated[
        Path,
        typer.Argument(
            help="The directory containing the source files.",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
):
    """Split pages and trips from source files into the `pages` and `trips` directories."""
    source_files = get_text_source_files(path_in=path_in)
    split_to_pages(source_paths=source_files)
    split_to_trips(source_paths=source_files)
    typer.echo(
        f"Split pages and trips for {len(source_files)} bid packages from {path_in}"
    )


if __name__ == "__main__":
    app()
