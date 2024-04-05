import pytest
from pathlib import Path
import os
import json
from puggle import Dataset

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_dataset"


@pytest.fixture
def dataset(request):
    return _get_dataset(request)


@pytest.fixture
def dataset_after(request):
    return _get_dataset(request)


@pytest.fixture
def dataset_json_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.json")


@pytest.fixture
def dataset_json_path_2(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.json")


@pytest.fixture
def dataset_csv_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


@pytest.fixture
def dataset_untyped_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}")


def _get_dataset(request):
    """Retrieve the given dataset. The format it will load (quickgraph or
    spert) will depend on the name of the dataset to load (if it contains
    "quickgraph", it will be loaded as quickgraph, otherwise it'll be loaded
    as spert).
    If name is empty, it will return an empty dataset.

    Args:
        request (TYPE): The request, i.e. the name of the dataset to load.

    Returns:
        Dataset: The dataset.
    """
    name = request.param

    data_format = "spert"
    if "quickgraph" in name:
        data_format = "quickgraph"

    if name == "empty":
        return Dataset()
    else:
        d = Dataset()
        d.load_documents(
            anns_filename=(os.path.join(FIXTURE_DIR, f"{name}.json")),
            anns_format=data_format,
        )
        return d
