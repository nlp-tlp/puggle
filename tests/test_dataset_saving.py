import json
import pytest
import os
from pathlib import Path
from puggle import Dataset


@pytest.mark.parametrize(
    "dataset, output_format, dataset_json_path",
    [
        ("medium", "quickgraph", "medium_after_save_quickgraph"),
        ("medium", "json", "medium_after_save_json"),
    ],
    indirect=["dataset", "dataset_json_path"],
)
def test_dataset_saving(dataset, output_format, dataset_json_path, tmp_path):
    out_path = tmp_path / "out.json"
    dataset.save_to_file(out_path, output_format=output_format)

    with open(out_path, "r") as f:
        j = json.load(f)

    # with open(f"test-{output_format}.json", "w") as f:
    #     json.dump(j, f, indent=2)

    assert open(out_path, "r").read() == open(dataset_json_path, "r").read()


@pytest.mark.parametrize(
    "dataset, output_format",
    [
        ("medium", "jsoon"),
        ("medium", "quackgraph"),
    ],
    indirect=["dataset"],
)
def test_dataset_saving_invalid_format(dataset, output_format, tmp_path):
    out_path = tmp_path / "out.json"
    with pytest.raises(ValueError):
        dataset.save_to_file(out_path, output_format=output_format)
