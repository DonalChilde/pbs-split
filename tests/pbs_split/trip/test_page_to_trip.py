from importlib import resources
from pathlib import Path

from tests.resources import RESOURCES_ANCHOR

from pbs_split.extract_trips import parse_trips_from_file, write_trips
from pbs_split.models import Trip

DATA_FILE_NAME = "PBS_DCA_May_2022_20220408124308.page_3_of_173.json"
DATA_FILE_PATH = "page"
DATA_FILE_ANCHOR = f"{DATA_FILE_PATH}/{DATA_FILE_NAME}"


def test_page_to_trips(test_output_dir: Path):
    file_resource = resources.files(RESOURCES_ANCHOR).joinpath(DATA_FILE_ANCHOR)
    with resources.as_file(file_resource) as input_path:
        path_out = test_output_dir / Path("trip/test_page_to_trip")
        trips = parse_trips_from_file(input_path)

        count = write_trips(
            file_stem=input_path.stem, trips=trips, path_out=path_out, overwrite=False
        )
        files_output = list(path_out.glob("*.trip_*"))
        assert len(files_output) == count
        assert count == 5
        trip = Trip.from_file(files_output[2])
        assert len(trip.lines.strings) > 5
