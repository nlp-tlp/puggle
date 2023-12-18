import pytest
from puggle import Dataset


def test_dataset_load_documents_invalid_args():
    d = Dataset()
    with pytest.raises(ValueError):
        d.load_documents(sd_filename=None, anns_filename=None)
        

# def test_neo4j_running_exception():
#     d = Dataset()
#     with pytest.raises(RuntimeError):
#         d.load_into_neo4j()


# Test that the dataset can be loaded into neo4j
@pytest.mark.parametrize(
    "dataset_json_path, dataset_csv_path, recreate",
    [
        ("empty_document", "empty_document", "True"),
        ("medium", "medium", "True"),           # recreate
        ("large", "large", "False"),            # no recreate
    ],
    indirect=["dataset_json_path", "dataset_csv_path"],
)
def test_dataset_load_into_neo4j(dataset_json_path, dataset_csv_path, recreate):
    d = Dataset()
    if dataset_json_path == "none":
        print(dataset_json_path, "dataset_json_path is none")
        with pytest.raises(ValueError):
            d.load_documents(
                sd_filename=dataset_csv_path,
                anns_format="spert",
            )
    else:
        d.load_documents(
            sd_filename=dataset_csv_path,
            anns_filename=dataset_json_path,
            anns_format="spert",
        )
    d.load_into_neo4j(recreate=recreate)
    

# Test that the dataset can be loaded into neo4j without annotations
@pytest.mark.parametrize(
    "dataset_csv_path",
    [
        ("empty_document"),
        ("medium"),
        ("large"),
    ],
    indirect=["dataset_csv_path"],
)
def test_dataset_load_into_neo4j_no_annotations(dataset_csv_path):
    d = Dataset()
    d.load_documents(
        sd_filename=dataset_csv_path,
        anns_format="spert",
    )
    d.load_into_neo4j(recreate=True)


