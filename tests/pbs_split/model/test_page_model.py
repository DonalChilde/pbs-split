import json
from dataclasses import asdict
from importlib import resources

from tests.resources import RESOURCES_ANCHOR

from pbs_split.models import Page

DATA_FILE_NAME = "PBS_DCA_February_2023_20230110102037.pdf.txt-page_2.json"
DATA_FILE_PATH = "page"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_load_page():
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        page = Page.from_file(input_path)
        page_json = json.loads(input_path.read_text(encoding="utf-8"))
        page_dict = asdict(page)
        assert page_json == page_dict
