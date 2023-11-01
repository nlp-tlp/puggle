import pytest
from puggle import Dataset


def test_dataset_load_documents_invalid_args():
    d = Dataset()
    with pytest.raises(ValueError):
        d.load_documents(sd_filename=None, anns_filename=None)
