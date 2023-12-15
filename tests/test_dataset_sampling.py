import pytest
import random
from puggle import Dataset, Document


random.seed(123)


# Test random sample
@pytest.mark.parametrize(
    "dataset, num_records",
    [
        ("medium", 1),
        ("large", 2),
        ("example_dataset_100", 10),
        ("example_dataset_500", 50)
    ],
    indirect=["dataset"],
)
def test_dataset_sampling_random_sample(dataset, num_records):
    rs_dataset = dataset.random_sample(num_records)
    assert len(rs_dataset.documents) == num_records
    assert all([doc in dataset.documents for doc in rs_dataset.documents])


# Test random split
@pytest.mark.parametrize(
    "dataset, num_train, num_dev, num_test",
    [
        ("small", 0, 0, 1),
        ("medium", 1, 0, 1),
        ("large", 2, 0, 1),
        ("example_dataset_100", 80, 10, 10),
        ("example_dataset_500", 400, 50, 50)
    ],
    indirect=["dataset"],
)
def test_dataset_sampling_random_split(dataset, num_train, num_dev, num_test):
    train, dev, test = dataset.random_split()
    print(len(train.documents), len(dev.documents), len(test.documents))

    assert len(train.documents) == num_train
    assert len(dev.documents) == num_dev
    assert len(test.documents) == num_test
    

# Test smart sample
@pytest.mark.parametrize(
    "dataset, num_records, num_samples",
    [
        ("empty_document", 1, 1),    # document with no tokens, mentions, relations
        ("medium", 1, 10),
        ("large", 2, 5),
        ("example_dataset_100", 10, 3), 
        ("example_dataset_500", 50, 1)
    ],
    indirect=["dataset"],
)
def test_dataset_sampling_smart_sample(dataset, num_records, num_samples):
    ss_dataset = dataset.smart_sample(num_records, num_samples)
    assert len(ss_dataset.documents) == num_records
    assert all([doc in dataset.documents for doc in ss_dataset.documents])




