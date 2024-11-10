from importlib import resources
from pathlib import Path

from tests.resources import RESOURCES_ANCHOR
from typer.testing import CliRunner

from pbs_split.cli.main_typer import app

DATA_FILE_PATH = "page"


def test_split_pages_to_trips(runner: CliRunner, test_output_dir: Path, capsys):
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_PATH)
    path_out = test_output_dir
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(app, ["trips", "split", str(input_path), str(path_out)])
        if result.stderr_bytes is not None:
            print(result.stderr)
        with capsys.disabled():
            print(result.stdout)
        assert result.exit_code == 0
        assert "Found 41 trips" in result.stdout
