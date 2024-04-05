import json
import pytest
import os
from puggle import Dataset


@pytest.mark.parametrize(
    "dataset, dataset_json_path, dataset_json_path_2",
    [
        (
            "sentence_splitting/sentence_splitting_before_quickgraph",
            "sentence_splitting/sentence_splitting_after_spert",
            "sentence_splitting/sentence_splitting_results",
        ),
        (
            "sentence_splitting/sentence_splitting_before_spert",
            "sentence_splitting/sentence_splitting_after_spert",
            "sentence_splitting/sentence_splitting_results",
        ),
        (
            "sentence_splitting/sentence_splitting_before_spert_complex",
            "sentence_splitting/sentence_splitting_after_spert_complex",
            "sentence_splitting/sentence_splitting_results_complex",
        ),
    ],
    indirect=["dataset", "dataset_json_path", "dataset_json_path_2"],
)
def test_dataset_saving(
    dataset, dataset_json_path, dataset_json_path_2, tmp_path
):
    """Ensure that the sentence splitting function works as expected."""
    out_path = tmp_path / "out.json"

    sentence_split_dataset, results = dataset.split_sentences(delimiter=".")
    sentence_split_dataset.save_to_file(out_path, output_format="spert")

    with open(dataset_json_path_2, "r", encoding="utf-8") as f:
        results_json = json.load(f)

    with open(out_path, "r", encoding="utf-8") as f:
        json.load(f)

    with open("temp_output.json", "w", encoding="utf-8") as f:
        sentence_split_dataset.save_to_file(
            "temp_output.json", output_format="spert"
        )

    for k, v in results_json.items():
        assert results[k] == v

    assert json.load(open(out_path, "r", encoding="utf-8")) == json.load(
        open(dataset_json_path, "r", encoding="utf-8")
    )
