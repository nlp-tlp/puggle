import pytest
from puggle import Dataset
import os
from py2neo import Graph
import pandas as pd


def test_dataset_load_documents_invalid_args():
    d = Dataset()
    with pytest.raises(ValueError):
        d.load_documents(sd_filename=None, anns_filename=None)
        

# Test that the dataset can be loaded into Neo4J
@pytest.mark.parametrize(
    "dataset, recreate, expected_node_count, expected_relation_count",
    [
        ("empty_document", "False", 0, 0),
        ("medium", "False", 8, 12),          # recreate
        ("large", "False", 12, 15),        # no recreate
        
    ],
    indirect=["dataset"],
)
def test_dataset_load_into_neo4j(dataset, recreate, expected_node_count, expected_relation_count):
    dataset.load_into_neo4j(recreate=recreate)
    
    port = os.getenv("NEO4J_PORT") if "NEO4J_PORT" in os.environ else 7687
    graph = Graph(password=os.getenv("NEO4J_PASSWORD"), port=port)
    node_count_query = "MATCH (n) RETURN COUNT(n) AS nodeCount"
    relation_count_query = "MATCH ()-[r]->() RETURN COUNT(r) AS relationCount"
    
    assert graph.run(node_count_query).evaluate() == expected_node_count
    assert graph.run(relation_count_query).evaluate() == expected_relation_count


# # Test that the dataset can be loaded into neo4j without annotations
# @pytest.mark.parametrize(
#     "dataset_json_path, expected_node_count, expected_relation_count",
#     [
#         ("empty_document", 0, 0),
#         ("small", 4, 5),
#         ("medium", 8, 12),
#         ("large", 12, 15),
#     ],
#     indirect=["dataset_json_path"],
# )
# def test_dataset_load_into_neo4j_no_annotations(dataset_json_path, expected_node_count, expected_relation_count):
#     d = Dataset()
#     d.load_documents(
#         anns_filename=dataset_json_path,
#         anns_format="spert",
#     )
#     d.load_into_neo4j(recreate=True)
    
#     port = os.getenv("NEO4J_PORT") if "NEO4J_PORT" in os.environ else 7687
#     graph = Graph(password=os.getenv("NEO4J_PASSWORD"), port=port)
#     node_count_query = "MATCH (n) RETURN COUNT(n) AS nodeCount"
#     relation_count_query = "MATCH ()-[r]->() RETURN COUNT(r) AS relationCount"
    
#     assert graph.run(node_count_query).evaluate() == expected_node_count
#     assert graph.run(relation_count_query).evaluate() == expected_relation_count
    

# Test generation of CSVs for Neo4J
@pytest.mark.parametrize(
    "dataset, expected_documents_csv, expected_entities_csv, expected_relations_csv, expected_document_entities_csv",
    [
        ("medium", "medium_documents", "medium_entities", "medium_relations", "medium_document_entities"),
        
    ],
    indirect=["dataset", "expected_documents_csv", "expected_entities_csv", "expected_relations_csv", "expected_document_entities_csv"],
)
def test_dataset_create_neo4j_csvs(dataset, expected_documents_csv, expected_entities_csv, expected_relations_csv, expected_document_entities_csv):
    # Create temporary paths for CSV files
    documents_path = "documents.csv"
    entities_path = "entities.csv"
    relations_path = "relations.csv"
    document_entities_path = "document_entities.csv"
    dataset.create_neo4j_csvs(documents_path, entities_path, relations_path, document_entities_path)
    
    # Perform assertions to check if the files are created and have the expected content
    assert os.path.exists(documents_path)
    assert os.path.exists(entities_path)
    assert os.path.exists(relations_path)
    assert os.path.exists(document_entities_path)
    
    assert open(documents_path).read() == open(expected_documents_csv).read()
    assert compare_csv_files(False, entities_path, expected_entities_csv)
    assert compare_csv_files(True, relations_path, expected_relations_csv)
    assert open(document_entities_path).read() == open(expected_document_entities_csv).read()
    
    # Clean up
    os.remove(documents_path)
    os.remove(entities_path)
    os.remove(relations_path)
    os.remove(document_entities_path)


def compare_csv_files(isRelation, file_path1, file_path2):
    # Read CSV files into DataFrames
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    
    # Drop the 'rel_idx' column
    if isRelation:
        df1 = df1.drop(columns=['rel_idx'])
        df2 = df2.drop(columns=['rel_idx'])

    # Sort DataFrames by all columns and reset index
    df1 = df1.sort_values(by=df1.columns.tolist()).reset_index(drop=True)
    df2 = df2.sort_values(by=df2.columns.tolist()).reset_index(drop=True)

    # Check if both DataFrames are equal
    are_equal = df1.equals(df2)

    return are_equal