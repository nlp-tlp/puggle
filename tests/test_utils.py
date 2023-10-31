import json
import pytest
from pathlib import Path
from puggle.utils import *

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_utils"


def _load_from_json_file(path: str):
    """Load the given JSON file into a list.

    Args:
        path (str): The path of the JSON file.

    Returns:
        list: The file, as a list (of dicts).
    """
    with open(FIXTURE_DIR / path) as f:
        return json.load(f)


def test_validate_anns_format():
    """Test validate_anns_format."""
    valid_formats = ["quickgraph", "spert"]
    invalid_formats = ["json", "test"]

    with pytest.raises(ValueError) as e:
        for f in invalid_formats:
            validate_anns_format(f)

    for f in valid_formats:
        validate_anns_format(f)


def test_normalise_annotation_format():
    """Test normalise_annotation_format."""

    qg_docs = _load_from_json_file("quickgraph_docs.json")
    spert_docs = _load_from_json_file("spert_docs.json")

    qg_docs_norm = [
        normalise_annotation_format(doc, "quickgraph") for doc in qg_docs
    ]
    spert_docs_norm = [
        normalise_annotation_format(doc, "spert") for doc in spert_docs
    ]

    # Ensure that every normalised QG doc is the same as every normalised
    # Spert doc.
    for qg_doc, spert_doc in zip(qg_docs_norm, spert_docs_norm):
        assert qg_doc == spert_doc
