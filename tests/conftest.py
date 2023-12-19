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
def dataset_csv_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


@pytest.fixture
def dataset_untyped_path(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}")


@pytest.fixture
def expected_documents_csv(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


@pytest.fixture
def expected_entities_csv(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


@pytest.fixture
def expected_relations_csv(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


@pytest.fixture
def expected_document_entities_csv(request):
    name = request.param
    return os.path.join(FIXTURE_DIR, f"{name}.csv")


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
