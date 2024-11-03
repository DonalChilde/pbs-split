from pathlib import Path


# pointless
def validate_dir_out(
    output_path: Path, *, exist_ok: bool = True, parents: bool = True
) -> bool:
    """Ensure that a path is a directory suitable for output.

    Optionally can ensure that parent directories exist.
    """
    if output_path.is_file():
        raise ValueError(
            f"{output_path} is an invalid destination. It is an existing file."
        )
    if output_path.is_dir() and not exist_ok:
        raise ValueError(
            f"{output_path} is an existing directory, and exists_ok is False."
        )
    output_path.mkdir(parents=parents, exist_ok=exist_ok)
    return True
