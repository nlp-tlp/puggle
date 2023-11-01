"""Utility functions such as normalising annotation formats, etc."""
from typing import Dict


def validate_anns_format(anns_format: str):
    """Helper function to ensure anns_format is valid.

    Args:
        anns_format (str): The format of the annotations.

    Raises:
        ValueError: If format not valid.
    """
    valid_formats = ["quickgraph", "spert"]
    if anns_format not in ["quickgraph", "spert"]:
        raise ValueError(f"anns_format must be in {valid_formats}.")


def normalise_annotation_format(doc: Dict, anns_format: str):
    """Normalise the given document (as a dict) into a uniform format.

    Args:
        doc (Dict): The document to normalise.
        anns_format (str): The annotation format.

    Returns:
        Dict: The normalised document.
    """
    validate_anns_format(anns_format)

    if anns_format == "quickgraph":
        return _normalise_quickgraph(doc)
    return _normalise_spert(doc)


def _normalise_spert(doc: Dict):
    """Normalise the spert-formatted JSON to be parsable by puggle.

    Args:
        doc (Dict): The annotations to parse.

    Returns:
        Dict: The parsed document.
    """
    if "entities" not in doc:
        doc["entities"] = []
    if "relations" not in doc:
        doc["relations"] = []

    for m in doc["entities"]:
        m["label"] = m["type"]
        del m["type"]

    for r in doc["relations"]:
        r["start"] = r["head"]
        r["end"] = r["tail"]
        del r["head"]
        del r["tail"]

    return doc


def _normalise_quickgraph(doc: Dict):
    """Normalise the quickgraph formatted JSON to be parsable by puggle.

    Args:
        doc (Dict): The annotations to parse.

    Returns:
        Dict: The parsed document.
    """
    if "entities" not in doc:
        doc["entities"] = []
    if "relations" not in doc:
        doc["relations"] = []

    entity_idxs = {}
    for i, m in enumerate(doc["entities"]):
        m["label"] = m["label"]
        entity_idxs[m["id"]] = i
        m["end"] = m["end"] + 1
        del m["id"]

    for r in doc["relations"]:
        r["start"] = entity_idxs[r["source_id"]]
        r["end"] = entity_idxs[r["target_id"]]
        r["type"] = r["label"]
        del r["label"]
        del r["source_id"]
        del r["target_id"]
        if "id" in r:
            del r["id"]

    return doc
