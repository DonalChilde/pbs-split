from importlib import resources
from pathlib import Path

from tests.resources import RESOURCES_ANCHOR
from typer.testing import CliRunner

from pbs_split.cli.main_typer import app

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.txt"
DATA_FILE_PATH = "full_package"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"
PAGE_COUNT = "174"


def test_split_pages(runner: CliRunner, test_output_dir: Path):
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    path_out = test_output_dir
    with resources.as_file(file_resource) as input_path:
        result = runner.invoke(app, ["pages", str(input_path), str(path_out)])
        if result.stderr_bytes is not None:
            print(result.stderr)
        print(result.stdout)
        assert result.exit_code == 0
        assert PAGE_COUNT in result.stdout
