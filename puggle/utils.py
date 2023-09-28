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
    validate_anns_format(anns_format)

    if anns_format == "quickgraph":
        return _normalise_quickgraph(doc)
    elif anns_format == "spert":
        return _normalise_spert(doc)

    return doc


def _normalise_spert(doc: Dict):
    """Normalise the spert-formatted JSON to be parsable by puggle.

    Args:
        doc (Dict): The annotations to parse.

    Returns:
        Dict: The parsed document.
    """
    for i, m in enumerate(doc["entities"]):
        m["labels"] = [m["type"]]
        del m["type"]

    for r in doc["relations"]:
        r["start"] = r["head"]
        r["end"] = r["tail"]

    return doc


def _normalise_quickgraph(doc: Dict):
    """Normalise the quickgraph formatted JSON to be parsable by puggle.

    Args:
        doc (Dict): The annotations to parse.

    Returns:
        Dict: The parsed document.
    """
    entity_idxs = {}
    for i, m in enumerate(doc["entities"]):
        m["labels"] = [m["label"]]
        del m["label"]
        entity_idxs[m["id"]] = i
        m["end"] = m["end"] + 1

    for r in doc["relations"]:
        r["start"] = entity_idxs[r["source_id"]]
        r["end"] = entity_idxs[r["target_id"]]
        r["type"] = r["label"]
        del r["label"]
        del r["source_id"]
        del r["target_id"]

    return doc
