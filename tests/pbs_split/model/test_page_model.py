import json
from dataclasses import asdict
from importlib import resources

from tests.resources import RESOURCES_ANCHOR

from pbs_split.snippets.indexed_string.model import IndexedStrings

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.page_1_of_173.json"
DATA_FILE_PATH = "page"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_load_page():
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        page = IndexedStrings.from_file(input_path)
        page_json = json.loads(input_path.read_text(encoding="utf-8"))
        page_dict = asdict(page)
        page_json["strings"] = tuple(page_json.get("strings"))
        assert page_json == page_dict
