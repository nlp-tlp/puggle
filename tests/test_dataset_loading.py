import json
import pytest
import os
from pathlib import Path
from puggle import Dataset

from .test_dataset import dataset_path, dataset_csv_path, dataset_full_path


@pytest.mark.parametrize(
    "dataset_path, error_type, error_msg",
    [
        ("invalid_mentions_1_missing_keys", KeyError, "missing keys"),
        ("invalid_mentions_2_missing_keys", KeyError, "missing keys"),
        (
            "invalid_mentions_3_invalid_start_index",
            ValueError,
            "start index cannot be the same as its end index",
        ),
    ],
    indirect=["dataset_path"],
)
def test_dataset_loading_invalid_mentions(dataset_path, error_type, error_msg):
    d = Dataset()
    with pytest.raises(error_type) as e:
        d.load_documents(anns_filename=dataset_path, anns_format="spert")
        assert error_msg in e.message


@pytest.mark.parametrize(
    "dataset_path, error_type, error_msg",
    [
        ("invalid_document_1_long_word", ValueError, "Word must be at most"),
        (
            "invalid_document_2_long_sentence",
            ValueError,
            "Sentence must contain at most",
        ),
        (
            "invalid_document_3_missing_tokens",
            ValueError,
            "Dictionary must contain tokens, entities, and relations",
        ),
    ],
    indirect=["dataset_path"],
)
def test_dataset_loading_invalid_documents(
    dataset_path, error_type, error_msg
):
    d = Dataset()
    with pytest.raises(error_type) as e:
        d.load_documents(anns_filename=dataset_path, anns_format="spert")
        assert error_msg in e.message


@pytest.mark.parametrize(
    "dataset_path, error_type, error_msg",
    [
        (
            "invalid_relations_1_mention_linked_to_itself",
            ValueError,
            "Cannot create relation between a mention and itself",
        ),
        (
            "invalid_relations_2_mention_missing",
            KeyError,
            "Mention corresponding to the relation",
        ),
        (
            "invalid_relations_3_no_entities",
            KeyError,
            "Mention corresponding to the relation",
        ),
    ],
    indirect=["dataset_path"],
)
def test_dataset_loading_invalid_relations(
    dataset_path, error_type, error_msg
):
    d = Dataset()
    with pytest.raises(error_type) as e:
        d.load_documents(anns_filename=dataset_path, anns_format="spert")
        assert error_msg in e.message


@pytest.mark.parametrize(
    "dataset_path, dataset_csv_path, num_documents, num_fields",
    [
        ("medium", "medium", 2, 4),
    ],
    indirect=["dataset_path", "dataset_csv_path"],
)
def test_dataset_loading_with_structured_data(
    dataset_path, dataset_csv_path, num_documents, num_fields
):
    d = Dataset()
    d.load_documents(
        sd_filename=dataset_csv_path,
        anns_filename=dataset_path,
        anns_format="spert",
    )
    assert len(d.documents) == num_documents
    assert len(d.documents[0].fields) == num_fields


@pytest.mark.parametrize(
    "dataset_path, dataset_full_path",
    [
        ("medium", "medium.pingu"),
        ("medium", "medium.csvv"),
    ],
    indirect=["dataset_path", "dataset_full_path"],
)
def test_dataset_loading_with_structured_data_non_csv(
    dataset_path, dataset_full_path
):
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(
            sd_filename=dataset_full_path,
            anns_filename=dataset_path,
            anns_format="spert",
        )


@pytest.mark.parametrize(
    "dataset_full_path, dataset_csv_path",
    [
        ("medium.pingu", "medium"),
    ],
    indirect=["dataset_full_path", "dataset_csv_path"],
)
def test_dataset_loading_with_annotated_data_non_json(
    dataset_full_path, dataset_csv_path
):
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(
            sd_filename=dataset_csv_path,
            anns_filename=dataset_full_path,
            anns_format="spert",
        )


@pytest.mark.parametrize(
    "dataset_path, dataset_csv_path",
    [
        ("medium", "medium_too_many_docs"),
        ("medium", "medium_not_enough_docs"),
    ],
    indirect=["dataset_path", "dataset_csv_path"],
)
def test_dataset_loading_with_mismatched_data(dataset_path, dataset_csv_path):
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(
            sd_filename=dataset_csv_path,
            anns_filename=dataset_path,
            anns_format="spert",
        )
        assert "Mismatch" in e.message


@pytest.mark.parametrize(
    "dataset_path, num_documents",
    [
        ("quickgraph", 2),
        ("quickgraph_no_annotators", 2),
        ("quickgraph_multiple_annotators", 4),
    ],
    indirect=["dataset_path"],
)
def test_dataset_loading_quickgraph(dataset_path, num_documents):
    """Ensure that a quickgraph-formatted annotations file can be loaded,
    even if it is not wrapped by an outer list with annotator keys.

    Args:
        dataset_path (str): The path from which to load the dataset.
    """
    d = Dataset()
    d.load_documents(
        anns_filename=dataset_path,
        anns_format="quickgraph",
    )
    print(d.documents)
    assert len(d.documents) == num_documents


def test_dataset_repr():
    d = Dataset()
    assert str(d) == "Dataset containing 0 documents."
