"""A dataset that stores tokens and labels in ET format."""
import os
import json
import csv
import random
import logging as logger
from json import JSONDecodeError
from typing import List
from py2neo import Graph
from dotenv import load_dotenv

from .Document import Document
from .Annotation import Annotation
from .utils import validate_anns_format, normalise_annotation_format

load_dotenv()


class Dataset(object):
    """A class representing a Dataset, which
    stores Documents in the form of Mentions and Relations.
    """

    def __init__(self):
        """Load a Dataset from a file path. The file must be .json.


        Args:
            filepath (os.path): The file path to load the dataset from.
        """
        super(Dataset, self).__init__()
        self.documents = []

    def save_to_file(self, filename: str):
        """Save the documents of this dataset to the given filename.

        Args:
            filename (str): The filename to save to.
        """
        with open(filename, "w") as f:
            json.dump([doc.to_dict() for doc in self.documents], f)

    def add_document(self, document: Document):
        """Add the given Document to this Dataset.

        Args:
            document (Document): The Document to add.

        """
        self.documents.append(document)

    def load_documents(
        self,
        sd_filename: os.path = None,
        anns_filename: os.path = None,
        anns_format: str = None,
    ):
        """Load a set of documents given the filepath of the structured data
        (a .csv file), and the filepath of the annotations (a .json file).
        Documents can still be created if either one of these is not present,
        but not if both are not present.
        Each row of each file must correspond to the other, e.g. row 3 of the
        structured data csv must correspond to row 3 of the annotations json.

        Args:
            sd_filename (os.path, optional): The filepath of the structured
               data.
            anns_filename (os.path, optional): The filepath of the
               annotations.
            anns_format (str): The format of the annotations file. Can be
               either "quickgraph" or "spert".
        """
        if sd_filename is None and anns_filename is None:
            raise ValueError(
                "Either sd_filename or anns_filename (or both) must be "
                "present in order to load Documents."
            )
        if anns_filename is not None:
            validate_anns_format(anns_format)

        structured_fields = []
        annotations = []

        if sd_filename is not None:
            structured_fields = self._load_structured_data(sd_filename)
        if anns_filename is not None:
            annotations = self._load_annotations(anns_filename, anns_format)

        if all((structured_fields, annotations)) and len(
            structured_fields
        ) != len(annotations):
            raise ValueError(
                "Mismatch between the length of the structured "
                "fields dataset and the annotations dataset."
            )

        if len(structured_fields) == 0:
            structured_fields = [None] * len(annotations)

        documents = []
        for sf, ann in zip(structured_fields, annotations):
            d = Document(sf, ann)
            documents.append(d)

        self.documents = documents

    def load_into_neo4j(self, recreate=False):
        """Load the Dataset into a Neo4j database.
        Automatically creates Nodes from the entities (mentions) appearing
        in each document, and relationships between them via the Relations.

        Args:
            recreate (bool, optional): If true, the Neo4j db will be cleared
                prior to inserting the documents into it.

        Raises:
            RuntimeError: If the Neo4j server is not running.
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
            # Create node for document
            cypher = f"MERGE (d:Document {{doc_idx: {i}}})"
            graph.run(cypher)

            ann = d.annotation
            # If this doc has no annotation, skip the creation of
            # entities and relationships
            if ann is None:
                continue

            # Update the Document node to copy over each of the fields
            # from the CSV dataset
            if d.fields:
                for k, v in d.fields.items():
                    val = ('"' + v + '"') if type(v) is str else v
                    cypher = (
                        f"MATCH (d:Document {{doc_idx: {i}}})\n"
                        f"SET d.{k} = {val}"
                    )
                    graph.run(cypher)

            # Do not continue building the graph if the annotation
            # has no relationships between entities
            if ann.relations is None:
                continue
            for rel in ann.relations:
                # Avoid cyclical relationships
                if rel.start.tokens == rel.end.tokens:
                    continue

                # Create relationship between head and tail
                cypher = (
                    f"MATCH (d:Document {{doc_idx: {i}}})\n"
                    f"MERGE (e1:Entity:{rel.start.get_first_label()} {{name: "
                    f"\"{' '.join(rel.start.tokens)}\"}})\n"
                    f"MERGE (e2:Entity:{rel.end.get_first_label()}  {{name: "
                    f"\"{' '.join(rel.end.tokens)}\"}})\n"
                    f"MERGE (e1)-[r:{rel.label}]->(e2)\n"
                    f"MERGE (e1)-[:APPEARS_IN]->(d)\n"
                    f"MERGE (e2)-[:APPEARS_IN]->(d)"
                )
                graph.run(cypher)
            if i > 0 and i % 10 == 0:
                print(f"Processed {i} documents")
        print("Graph creation complete.")

    def create_neo4j_csvs():
        """A function to generate a set of CSVs to load into Neo4j via
        IMPORT statements (an alternative for those who want to be able
        to save their graph to disk somehow and import it later/elsewhere).

        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError

    def _load_structured_data(self, filename: os.path):
        """Load a list of structured data from the given file.
        File must be a .csv file. The first row of the file should be
        a header with the names of each column.

        Args:
            filename (os.path): The filename to load.

        Returns:
            List[Dict]: A list of rows, where each row contains {k : v}
               pairs for each field.

        Raises:
            ValueError: If the file is not a .csv file.
        """
        if not filename.endswith(".csv"):
            raise ValueError("File must be a CSV file.")

        documents = []
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                documents.append(row)
        return documents

    def _load_annotations(self, filename: os.path, anns_format: str):
        """Load a list of annotations from the given file.
        File must be a .json file. Each annotation must be in the correct
        format, e.g:

            [{
                "tokens": ["one", "three", "two"],
                "mentions": [
                    { "start": 0, "end": 1, "labels": ["number"] },
                    { "start": 1, "end": 2, "labels": ["number"] },
                    { "start": 2, "end": 3, "labels": ["number"] }
                ],
                "relations": [
                    { "start": 1, "end": 0, "type": "bigger_than" },
                    { "start": 1, "end": 2, "type": "bigger_than" }
                ]
            }, ...]

        Args:
            filename (os.path): The filename to load.
            format (str): The format of the annotations. Can be either
               'quickgraph' or 'spert'.

        Returns:
            list: A list of Annotations.

        Raises:
            ValueError: If the file is not a JSON file, or fails to parse.
        """
        if not filename.endswith(".json"):
            raise ValueError("File must be a JSON file.")
        annotations = []
        with open(filename, "r") as f:
            try:
                d = json.load(f)

                # If using quickgraph format, combine all the annotations
                # into one single list.
                if anns_format == "quickgraph":
                    if len(d.keys()) > 1:
                        print(
                            "Warning: you appear to be loading "
                            "multiple annotators' annotations."
                            "This may result in duplicate nodes - "
                            "see the readme for more details."
                        )
                    anns = []
                    for k, v in d.items():
                        anns += v
                else:
                    anns = d

                for i, ann in enumerate(anns):
                    doc = normalise_annotation_format(ann, anns_format)

                    annotations.append(Annotation.from_dict(ann))

            except (JSONDecodeError, ValueError) as e:
                raise ValueError(
                    f"The .json file ({os.path.basename(filename)}) "
                    f"failed to parse due to the following issue: {e}"
                )
        logger.debug(f"Loaded {len(annotations)} annotations from {filename}.")
        return annotations

    def __repr__(self):
        """String representation of the dataset.

        Returns:
            str: String representation of the dataset.
        """
        return f"Dataset containing {len(self.documents)} documents."
