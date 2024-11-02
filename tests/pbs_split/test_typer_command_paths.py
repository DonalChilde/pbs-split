"""Test cases for the cli app default path."""

from typer.testing import CliRunner

from pbs_split.cli.main_typer import app


def test_app(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
    # assert False


def test_default_options(runner: CliRunner) -> None:

    result = runner.invoke(app, ["-vvv", "hello", "Bob"])
    assert "Verbosity: 3" in result.stdout
    print(result.stdout)
    if result.stderr_bytes is not None:
        print(result.stderr)
    assert result.exit_code == 0
