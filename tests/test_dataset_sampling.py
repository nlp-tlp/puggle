import json
import pytest
import os
import random
from pathlib import Path

random.seed(123)


@pytest.mark.parametrize(
    "dataset, num_records",
    [("medium", 1)],
    indirect=["dataset"],
)
def test_dataset_sampling_random_sample(dataset, num_records):
    rs = dataset.random_sample(num_records)
    assert len(rs.documents) == num_records
    assert all([doc in dataset.documents for doc in rs.documents])
