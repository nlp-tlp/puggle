import json
import pytest
import os
from pathlib import Path
from puggle import Dataset

from .test_dataset import dataset_path


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


def test_dataset_repr():
    d = Dataset()
    assert str(d) == "Dataset containing 0 documents."
