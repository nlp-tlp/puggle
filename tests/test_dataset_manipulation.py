import json
import pytest
import os
from pathlib import Path

from .test_dataset import dataset, dataset_after


@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("empty", "number", "empty"),
        ("small", "number", "small_after_drop_ec"),
        ("medium", "number", "medium_after_drop_ec"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_entity_class(dataset, drop_class, dataset_after):
    dataset.drop_entity_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("empty", "x", "empty"),
        ("small", "x", "small"),
        ("medium", "x", "medium"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_missing_relation_class(
    dataset, drop_class, dataset_after
):
    dataset.drop_relation_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("empty", "bigger_than", "empty"),
        ("small", "bigger_than", "small_after_drop_rc"),
        ("medium", "bigger_than", "medium_after_drop_rc"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_relation_class(dataset, drop_class, dataset_after):
    dataset.drop_relation_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, class_from, class_to, dataset_after",
    [
        ("empty", "number", "pingu", "empty"),
        ("small", "number", "pingu", "small_after_convert_ec"),
        ("medium", "noise", "pingu", "medium_after_convert_ec"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_convert_entity_class(
    dataset, class_from, class_to, dataset_after
):
    dataset.convert_entity_class(class_from, class_to)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, class_from, class_to, dataset_after",
    [
        ("empty", "bigger_than", "pingu", "empty"),
        ("small", "bigger_than", "pingu", "small_after_convert_rc"),
        ("medium", "bigger_than", "pingu", "medium_after_convert_rc"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_convert_relation_class(
    dataset, class_from, class_to, dataset_after
):
    dataset.convert_relation_class(class_from, class_to)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, dataset_after",
    [
        ("empty", "empty"),
        ("small", "small"),  # Small and medium should be unaffected
        ("medium", "medium"),
        ("hierarchical", "hierarchical_after_flatten_ec"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_flatten_all_entities(dataset, dataset_after):
    dataset.flatten_all_entities()
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, dataset_after",
    [
        ("empty", "empty"),
        ("small", "small"),  # Small and medium should be unaffected
        ("medium", "medium"),
        ("hierarchical", "hierarchical_after_flatten_rc"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_flatten_all_relations(dataset, dataset_after):
    dataset.flatten_all_relations()
    assert dataset.to_list() == dataset_after.to_list()
