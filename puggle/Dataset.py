"""A dataset that stores tokens and labels in ET format."""
import os
import json
import random
import logging as logger
from json import JSONDecodeError
from typing import List
from py2neo import Graph
from dotenv import load_dotenv

from .Document import Document

load_dotenv()


class Dataset(object):
    """A class representing a Dataset, which
    stores Documents in the form of Mentions and Relations.
    """

    def __init__(self, filepath):
        """Load a Dataset from a file path. The file must be .json.


        Args:
            filepath (os.path): The file path to load the dataset from.
        """
        super(Dataset, self).__init__()
        self.documents = self._load_documents_from_file(filepath)

    def save_to_file(self, filename: str):
        """Save the documents of this dataset to the given filename.

        Args:
            filename (str): The filename to save to.
        """
        with open(filename, "w") as f:
            json.dump([doc.to_dict() for doc in self.documents], f)

    def flatten(self):
        """Flatten the dataset, i.e. ensure every mention has only one
        label.
        """
        for doc in self.documents:
            doc.flatten()

    def load_into_neo4j(self, recreate=False):
        """Load the Dataset into a Neo4j database.
        Automatically creates Nodes from the entities (mentions) appearing
        in each document, and relationships between them via the Relations.

        Raises:
            RuntimeError: If the Neo4j server is not running.

        Args:
            recreate (bool, optional): If true, the Neo4j db will be
               cleared prior to inserting the documents into it.
        """

        port = os.getenv("NEO4J_PORT") if "NEO4J_PORT" in os.environ else 7687

        # Init graph
        graph = Graph(
            password=os.getenv("NEO4J_PASSWORD"),
            port=port,
        )

        # Attempt to run a query to make sure it is working
        try:
            graph.run("MATCH () RETURN 1 LIMIT 1")
        except Exception as e:
            raise RuntimeError(
                "The Neo4j graph does not appear to be running. "
                f"Please run Neo4j on port {port} to proceed."
            )

        if recreate:
            graph.run("MATCH (n) DETACH DELETE (n)")

        for i, d in enumerate(self.documents):
            if d.relations is None:
                continue
            for rel in d.relations:
                # Avoid cyclical relationships
                if rel.start.tokens == rel.end.tokens:
                    continue

                # Create relationship between head and tail
                cypher = (
                    f"MERGE (e1:Entity:{rel.start.get_first_label()} {{name: "
                    f"\"{' '.join(rel.start.tokens)}\"}})\n"
                    f"MERGE (e2:Entity:{rel.end.get_first_label()}  {{name: "
                    f"\"{' '.join(rel.end.tokens)}\"}})\n"
                    f"MERGE (e1)-[r:{rel.label}]->(e2)"
                )
                graph.run(cypher)
                if i > 0 and i % 10 == 0:
                    print(f"Processed {i} documents")
        print("Graph creation complete.")

    def _load_documents_from_file(self, filename: os.path):
        """Load a list of Document objects from the given file.

        Args:
            filename (str): The filename to load from.

        Returns:
            list: A list of Documents.
        """
        documents = []
        with open(filename, "r") as f:
            try:
                d = json.load(f)
                for i, doc in enumerate(d):
                    documents.append(Document.from_dict(doc, doc_idx=i))

            except (JSONDecodeError, ValueError) as e:
                raise ValueError(
                    f"The .json file ({os.path.basename(filename)}) "
                    f"failed to parse due to the following issue: {e}"
                )
        logger.debug(f"Loaded {len(documents)} documents from {filename}.")
        return documents

    def __repr__(self):
        """String representation of the dataset.

        Returns:
            str: String representation of the dataset.
        """
        return f"Dataset containing {len(self.documents)} documents."
