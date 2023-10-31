import json
import pytest
import os
from pathlib import Path
from puggle import Dataset

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_dataset"


@pytest.fixture
def dataset(request):
    return _get_dataset(request)


@pytest.fixture
def dataset_after(request):
    return _get_dataset(request)


@pytest.fixture
def dataset_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.json")


@pytest.fixture
def dataset_csv_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


@pytest.fixture
def dataset_full_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}")


def _get_dataset(request):
    name = request.param
    if name == "empty":
        return Dataset()
    else:
        d = Dataset()
        d.load_documents(
            anns_filename=(os.path.join(FIXTURE_DIR, f"{name}.json")),
            anns_format="spert",
        )
        return d


def test_dataset_load_documents_invalid_args():
    d = Dataset()
    with pytest.raises(ValueError):
        d.load_documents(sd_filename=None, anns_filename=None)
