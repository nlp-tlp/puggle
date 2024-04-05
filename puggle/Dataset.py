"""A Dataset that stores a list of Documents.
"""
import os
import json
import csv
import logging as logger
from json import JSONDecodeError
from typing import Dict, List
from py2neo import Graph
from dotenv import load_dotenv

from .Document import Document
from .Annotation import Annotation
from .utils import (
    validate_anns_format,
    normalise_annotation_format,
)
from .logger import logger

load_dotenv()


class Dataset(object):
    """A class representing a Dataset, which stores a list of Documents.

    :var documents: A List of :class:`puggle.Document.Document` objects.
    """

    def __init__(self):
        """Create an empty Dataset. Documents may be loaded via the
        :func:`puggle.Dataset.Dataset.load_documents` function.
        """
        super().__init__()
        self.documents = []

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

        self.documents += documents
        logger.info(
            f"Successfully loaded {len(documents)} documents. "
            f"Dataset now contains {len(self.documents)} documents in total."
        )

    def save_to_file(self, filename: str, output_format: str = "json"):
        """Save the documents of this dataset to the given filename.

        There are two `output_format` options to choose from: `json`
        and `quickgraph`. See the "Basic functionality" section of the
        documentation for more info.

        Args:
            filename (str): The filename to save to.
            output_format (str): The format to save to. 'json' will save as a
               json file without any special formatting. 'spert' will save it
               ready for using in SPERT. 'quickgraph' will save
               as a json file that can be loaded directly into quickgraph.
        """
        if output_format not in ["json", "spert", "quickgraph"]:
            raise ValueError(
                "Output format must be either 'json', 'spert' or 'quickgraph'"
            )

        if output_format == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    [doc.to_dict() for doc in self.documents], f, indent=2
                )
        elif output_format == "spert":
            spert_docs = _to_spert(self)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(spert_docs, f, indent=2)
        elif output_format == "quickgraph":
            quickgraph_docs = _to_quickgraph(self)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(quickgraph_docs, f, indent=2)

        logger.info(f"Saved dataset to %s." % filename)

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
                    f"MERGE (e1:Entity:{rel.start.label} {{name: "
                    f"\"{' '.join(rel.start.tokens)}\"}})\n"
                    f"MERGE (e2:Entity:{rel.end.label}  {{name: "
                    f"\"{' '.join(rel.end.tokens)}\"}})\n"
                    f"MERGE (e1)-[r:{rel.label}]->(e2)\n"
                    f"MERGE (e1)-[:APPEARS_IN]->(d)\n"
                    f"MERGE (e2)-[:APPEARS_IN]->(d)"
                )
                graph.run(cypher)
            if i > 0 and i % 1000 == 0:
                logger.info(f"Processed {i} documents")
        logger.info("Graph creation complete.")

    def add_document(self, document: Document):
        """Add the given Document to this Dataset.

        Args:
            document (Document): The Document to add.

        """
        self.documents.append(document)

    def create_neo4j_csvs(
        self,
        documents_path: str,
        entities_path: str,
        relations_path: str,
        document_entities_path: str,
    ):
        """A function to generate a set of CSVs to load into Neo4j via
        IMPORT statements (an alternative for those who want to be able
        to save their graph to disk somehow and import it later/elsewhere).


        Args:
            documents_path (str): Path to save the documents (CSV).
            entities_path (str): Path to save the entities (CSV).
            relations_path (str): Path to save the relations (CSV).
            document_entities_path (str): Path to save the relationships
              between entities and the documents in which they appear (CSV).
        """

        docs = set()
        ents = set()
        rels = set()
        doc_ents = set()
        ent_idxs = {}
        rel_freqs = {}

        document_fieldnames = []

        for i, d in enumerate(self.documents):
            if i == 0:
                print(d.fields)
                document_fieldnames = d.fields.keys()
            ann = d.annotation

            docs.add(tuple([i, *d.fields.values()]))

            for mention in ann.mentions:
                t = tuple([mention.label, " ".join(mention.tokens)])
                ents.add(t)
                if t not in ent_idxs:
                    ent_idxs[t] = len(ent_idxs)
                doc_ents.add(tuple([i, ent_idxs[t]]))

            for rel in ann.relations:
                e1_idx = ent_idxs[
                    tuple([rel.start.label, " ".join(rel.start.tokens)])
                ]
                e2_idx = ent_idxs[
                    tuple([rel.end.label, " ".join(rel.end.tokens)])
                ]

                t = tuple(
                    [
                        e1_idx,
                        e2_idx,
                        rel.start.label,
                        " ".join(rel.start.tokens),
                        rel.end.label,
                        " ".join(rel.end.tokens),
                        rel.label,
                    ]
                )
                if t not in rel_freqs:
                    rel_freqs[t] = 0
                rel_freqs[t] += 1
                rels.add(t)

        with open(documents_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["doc_idx", *document_fieldnames])
            for row in list(docs):
                writer.writerow(row)
            logger.info(
                "Saved %d documents to %s." % (len(docs), documents_path)
            )

        with open(entities_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["entity_idx", "label", "tokens"])
            for i, row in enumerate(list(ents)):
                writer.writerow([ent_idxs[row]] + list(row))
            logger.info(
                "Saved %d entities to %s." % (len(ents), entities_path)
            )

        with open(relations_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "rel_idx",
                    "e1_idx",
                    "e2_idx",
                    "e1_label",
                    "e1_tokens",
                    "e2_label",
                    "e2_tokens",
                    "rel_label",
                    "frequency",
                ]
            )
            for i, row in enumerate(list(rels)):
                writer.writerow([i] + list(row) + [rel_freqs[row]])
            logger.info(
                "Saved %d relations to %s." % (len(rels), relations_path)
            )

        with open(
            document_entities_path, "w", newline="", encoding="utf-8"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["doc_idx", "entity_idx"])
            for row in list(doc_ents):
                writer.writerow(row)
            logger.info(
                "Saved %d document entities to %s."
                % (len(doc_ents), document_entities_path)
            )

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
        with open(filename, "r", encoding="utf-8") as f:
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
                    { "start": 0, "end": 1, "label": "number" },
                    { "start": 1, "end": 2, "label": "number" },
                    { "start": 2, "end": 3, "label": "number" }
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
        with open(filename, "r", encoding="utf-8") as f:
            try:
                d = json.load(f)

                # If using quickgraph format, combine all the annotations
                # into one single list.
                if anns_format == "quickgraph":
                    anns = []
                    if isinstance(d, list):
                        anns = d
                    else:
                        if len(d.keys()) > 1:
                            logger.warning(
                                "Warning: you appear to be loading "
                                "multiple annotators' annotations."
                                "This may result in duplicate nodes - "
                                "see the readme for more details."
                            )
                        anns = []
                        for _, v in d.items():
                            anns += v
                else:
                    anns = d

                for ann in anns:
                    # Ignore unsaved annotations in QuickGraph
                    if (
                        anns_format == "quickgraph"
                        and "saved" in ann
                        and not ann["saved"]
                    ):
                        continue
                    normalise_annotation_format(ann, anns_format)

                    annotations.append(Annotation.from_dict(ann))

            except (JSONDecodeError, ValueError) as e:
                raise ValueError(
                    f"The .json file ({os.path.basename(filename)}) "
                    f"failed to parse due to the following issue: {e}"
                )
        logger.debug(f"Loaded {len(annotations)} annotations from {filename}.")
        return annotations

    def get_stats(self):
        """Return a string of some useful stats of this dataset.

        Returns:
            str: Stats (num docs, mentions, rels)
        """
        num_mentions = sum(
            [len(doc.annotation.mentions) for doc in self.documents]
        )
        num_relations = sum(
            [len(doc.annotation.relations) for doc in self.documents]
        )

        return (
            f"Dataset containing {len(self.documents)} documents, "
            f" {num_mentions} mentions, and {num_relations} relations."
        )

    def __repr__(self):
        """String representation of the dataset.

        Returns:
            str: String representation of the dataset.
        """
        return f"Dataset containing {len(self.documents)} documents."

    def to_list(self):
        """Return a list representation of this dataset.

        Returns:
            list[Dict]: A list of Dicts, where each Dict is one document from
               this dataset.
        """
        return [doc.to_dict() for doc in self.documents]


def _to_quickgraph(dataset: Dataset) -> List[Dict]:
    """Convert the given Dataset to a list of dicts compatible with Quickgraph.

    Args:
        dataset (Dataset): The dataset to convert.

    Returns:
        List[Dict]: A list of Quickgraph-compatible data.
    """
    quickgraph_docs = []
    for doc in dataset.documents:
        ann = doc.annotation

        entities = []
        relations = []

        for i, m in enumerate(ann.mentions):
            entities.append(
                {
                    "id": str(i + 1),
                    "start": m.start,
                    "end": m.end - 1,
                    "label": m.label,
                }
            )

        for i, r in enumerate(ann.relations):
            relations.append(
                {
                    "source_id": str(r.start.mention_id + 1),
                    "target_id": str(r.end.mention_id + 1),
                    "label": r.label,
                }
            )

        qd = {
            "original": " ".join(ann.tokens),
            "tokens": ann.tokens,
            "entities": entities,
            "relations": relations,
        }
        quickgraph_docs.append(qd)
    return quickgraph_docs


def _to_spert(dataset: Dataset) -> List[Dict]:
    """Convert the given Dataset to a list of dicts compatible with SPERT.

    Args:
        dataset (Dataset): The dataset to convert.

    Returns:
        List[Dict]: A list of SPERT-compatible data.
    """
    spert_docs = []
    for doc in dataset.documents:
        ann = doc.annotation

        entities = []
        relations = []

        for m in ann.mentions:
            entities.append(
                {
                    "start": m.start,
                    "end": m.end,
                    "type": m.label,
                }
            )

        for i, r in enumerate(ann.relations):
            relations.append(
                {
                    "head": r.start.mention_id,
                    "tail": r.end.mention_id,
                    "type": r.label,
                }
            )

        sd = {
            "tokens": ann.tokens,
            "entities": entities,
            "relations": relations,
        }
        # If the document has a document index (after sentence splitting),
        # carry that through to the output
        if doc.document_index is not None:
            sd["document_index"] = doc.document_index
        spert_docs.append(sd)

    return spert_docs
