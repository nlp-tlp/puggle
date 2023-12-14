import json
import pytest
import os
from pathlib import Path
from puggle import Dataset


@pytest.mark.parametrize(
    "dataset, output_format, dataset_json_path",
    [
        ("medium", "json", "medium_after_save_json"),
        ("medium", "spert", "medium_after_save_spert"),
        ("medium", "quickgraph", "medium_after_save_quickgraph"),
        ("sampleset", "json", "sampleset_after_save_json"),
        ("sampleset", "spert", "sampleset_after_save_spert"),
        ("sampleset", "quickgraph", "sampleset_after_save_quickgraph"),
    ],
    indirect=["dataset", "dataset_json_path"],
)
def test_dataset_saving(dataset, output_format, dataset_json_path, tmp_path):
    out_path = tmp_path / "out.json"
    dataset.save_to_file(out_path, output_format=output_format)
    
    assert out_path.exists()

    with open(out_path, "r") as f:
        saved_data  = json.load(f)
        
    with open(dataset_json_path, "r") as f:
        original_data = json.load(f)
        
    assert saved_data == original_data
    assert open(out_path, "r").read() == open(dataset_json_path, "r").read()

@pytest.mark.parametrize(
    "dataset, output_format",
    [
        ("medium", "jsoon"),
        ("sampleset", "quackgraph"),
    ],
    indirect=["dataset"],
)
def test_dataset_saving_invalid_format(dataset, output_format, tmp_path):
    out_path = tmp_path / "out.json"
    with pytest.raises(ValueError):
        dataset.save_to_file(out_path, output_format=output_format)

def test_dataset_saving_empty_dataset(tmp_path):
    out_path = tmp_path / "empty_out.json"
    empty_dataset = Dataset()
    empty_dataset.save_to_file(out_path, output_format="json")

    assert out_path.exists()

    with open(out_path, "r") as f:
        saved_data = json.load(f)

    assert saved_data == []