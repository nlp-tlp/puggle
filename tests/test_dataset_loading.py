import json
import pytest
import os
from pathlib import Path
from puggle import Dataset

# Test that ValueError is raised when both sd_filename and anns_filename are None
def test_dataset_loading_no_filenames():
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents()
        assert "Either sd_filename or anns_filename (or both) must be present in order to load Documents." in str(e.value)

# Test that ValueError is raised when an invalid anns_format is provided
# !! Update the filename
def test_dataset_loading_invalid_anns_format():
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(sd_filename="medium.csv", anns_filename="medium.json", anns_format="invalid_format")
        assert "anns_format must be in" in str(e.value)

# Test that ValueError is raised when there is a mismatch in the length of structured fields and annotations
@pytest.mark.parametrize(
    "dataset_json_path, dataset_csv_path",
    [
        ("medium", "medium_too_many_docs"),
        ("medium", "medium_not_enough_docs"),
    ],
    indirect=["dataset_json_path", "dataset_csv_path"],
)
def test_dataset_loading_mismatched_data(dataset_json_path, dataset_csv_path):
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(
            sd_filename=dataset_csv_path,
            anns_filename=dataset_json_path,
            anns_format="spert",
        )
        assert "Mismatch between the length of the structured fields dataset and the annotations dataset." in str(e.value)

# Test for loading a dataset with invalid mentions 
@pytest.mark.parametrize(
    "dataset_json_path, error_type, error_msg",
    [
        ("invalid_mentions_1_missing_keys", KeyError, "missing keys"),
        ("invalid_mentions_2_missing_keys", KeyError, "missing keys"),
        ("invalid_mentions_3_invalid_start_index", ValueError, "Mention start index cannot be the same as its end index"),
    ],
    indirect=["dataset_json_path"],
)
def test_dataset_loading_invalid_mentions(dataset_json_path, error_type, error_msg):
    d = Dataset()
    with pytest.raises(error_type) as e:
        d.load_documents(anns_filename=dataset_json_path, anns_format="spert")
        assert error_msg in e.message

# Test for loading a dataset with invalid relations
@pytest.mark.parametrize(
    "dataset_json_path, error_type, error_msg",
    [
        ("invalid_relations_1_mention_linked_to_itself", ValueError, "Cannot create relation between a mention and itself"),
        ("invalid_relations_2_mention_missing", KeyError, "mention corresponding to the relation"),
        ("invalid_relations_3_no_entities", KeyError, "mention corresponding to the relation"),
    ],
    indirect=["dataset_json_path"],
)
def test_dataset_loading_invalid_relations(dataset_json_path, error_type, error_msg):
    d = Dataset()
    with pytest.raises(error_type) as e:
        d.load_documents(anns_filename=dataset_json_path, anns_format="spert")
        assert error_msg in e.message

# Test for loading a dataset with invalid documents
@pytest.mark.parametrize(
    "dataset_json_path, error_type, error_msg",
    [
        ("invalid_document_1_long_word", ValueError, "Word must be at most"),
        ("invalid_document_2_long_sentence", ValueError, "Sentence must contain at most"),
        ("invalid_document_3_missing_tokens", ValueError, "Dictionary must contain tokens, entities, and relations"),
    ],
    indirect=["dataset_json_path"],
)
def test_dataset_loading_invalid_documents(dataset_json_path, error_type, error_msg):
    d = Dataset()
    with pytest.raises(error_type) as e:
        d.load_documents(anns_filename=dataset_json_path, anns_format="spert")
        assert error_msg in e.message

# Test for loading a dataset with structured data
@pytest.mark.parametrize(
    "dataset_json_path, dataset_csv_path, num_documents, num_fields",
    [
        ("medium", "medium", 2, 4),
        ("sampleset", "sampleset", 3, 5),
    ],
    indirect=["dataset_json_path", "dataset_csv_path"],
)
def test_dataset_loading_with_structured_data(dataset_json_path, dataset_csv_path, num_documents, num_fields):
    d = Dataset()
    d.load_documents(
        sd_filename=dataset_csv_path,
        anns_filename=dataset_json_path,
        anns_format="spert",
    )
    assert len(d.documents) == num_documents
    assert len(d.documents[0].fields) == num_fields

# Test for correct file format for structured data (CSV)
@pytest.mark.parametrize(
    "dataset_json_path, dataset_untyped_path",
    [
        ("medium", "medium.pingu"),
        ("medium", "medium.csvv"),
    ],
    indirect=["dataset_json_path", "dataset_untyped_path"],
)
def test_dataset_loading_with_structured_data_non_csv(dataset_json_path, dataset_untyped_path):
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(
            sd_filename=dataset_untyped_path,
            anns_filename=dataset_json_path,
            anns_format="spert",
        )
        assert "File must be a CSV file." in e.message

# Test for correct file format for annotations (JSON)
@pytest.mark.parametrize(
    "dataset_untyped_path, dataset_csv_path",
    [
        ("medium.pingu", "medium"),
        ("medium.jsonn", "medium"),
    ],
    indirect=["dataset_untyped_path", "dataset_csv_path"],
)
def test_dataset_loading_with_annotated_data_non_json(
    dataset_untyped_path, dataset_csv_path
):
    d = Dataset()
    with pytest.raises(ValueError) as e:
        d.load_documents(
            sd_filename=dataset_csv_path,
            anns_filename=dataset_untyped_path,
            anns_format="spert",
        )
        assert "File must be a JSON file." in e.message


@pytest.mark.parametrize(
    "dataset_json_path, num_documents",
    [
        ("quickgraph", 2),
        ("quickgraph_no_annotators", 2),
        ("quickgraph_multiple_annotators", 4),
    ],
    indirect=["dataset_json_path"],
)
def test_dataset_loading_quickgraph(dataset_json_path, num_documents):
    """Ensure that a quickgraph-formatted annotations file can be loaded,
    even if it is not wrapped by an outer list with annotator keys.

    Args:
        dataset_json_path (str): The path from which to load the dataset.
    """
    d = Dataset()
    d.load_documents(
        anns_filename=dataset_json_path,
        anns_format="quickgraph",
    )
    assert len(d.documents) == num_documents

def test_dataset_repr():
    d = Dataset()
    assert str(d) == "Dataset containing 0 documents."
