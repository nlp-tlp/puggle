import json
import pytest
import os
from pathlib import Path


@pytest.mark.parametrize(
    "dataset, expected",
    [("empty", 0), ("small", 3)],
    indirect=["dataset"],
)
def test_dataset_stats_get_unique_tokens_count(dataset, expected):
    assert dataset.get_unique_tokens_count() == expected


@pytest.mark.parametrize(
    "dataset, expected",
    [
        ("empty", []),
        ("small", [("number", 3)]),
        ("medium", [("number", 4), ("noise", 4)]),
    ],
    indirect=["dataset"],
)
def test_dataset_stats_get_entity_label_counts(dataset, expected):
    assert dataset.get_entity_label_counts() == expected


@pytest.mark.parametrize(
    "dataset, expected",
    [
        ("empty", []),
        ("small", [("number", 1)]),
        ("medium", [("number", 2), ("noise", 1)]),
    ],
    indirect=["dataset"],
)
def test_dataset_stats_get_entity_label_counts_dl(dataset, expected):
    assert dataset.get_entity_label_counts(document_level=True) == expected
