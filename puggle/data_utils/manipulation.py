"""Tools for manipulating Puggle datasets. When this library is imported,
the functions will be added to the Dataset class."""
from puggle import Dataset
from puggle.logger import logger


def drop_entity_class(self: Dataset, entity_class: str):
    """
    :bdg-success-line:`Manipulation`
    Remove any instances of the given entity class from the mentions of this
    Dataset.
    Also remove all Relations referencing the deleted mentions.

    Args:
        entity_class (str): The entity class to remove.
    """
    dataset = self
    n_removed_e = 0
    n_removed_r = 0
    for doc in dataset.documents:
        a = doc.annotation

        updated_mentions = list(
            filter(lambda m: m.label != entity_class, a.mentions)
        )
        n_removed_e += len(a.mentions) - len(updated_mentions)
        a.mentions = updated_mentions

        # Remove connected relations
        updated_relations = list(
            filter(
                lambda r: ((r.start in a.mentions) or (r.end in a.mentions)),
                a.relations,
            )
        )
        n_removed_r += len(a.relations) - len(updated_relations)
        a.relations = updated_relations

    logger.info(
        f'Drop Entity class "{entity_class}": removed {n_removed_e} entities '
        f"and {n_removed_r} connected relations."
    )


def drop_relation_class(self: Dataset, relation_class: str):
    """
    :bdg-success-line:`Manipulation`
    Remove any instances of the given relation class from the relations of
    this Dataset.

    Args:
        relation_class (str): The relation class to remove.
    """
    dataset = self
    n_removed = 0
    for doc in dataset.documents:
        a = doc.annotation
        n_removed += sum(r.label == relation_class for r in a.relations)
        a.relations = list(
            filter(lambda r: r.label != relation_class, a.relations)
        )

    logger.info(
        f'Drop Relation class "{relation_class}": removed {n_removed} relations.'
    )


def convert_entity_class(self: Dataset, original_ec: str, modified_ec: str):
    """
    :bdg-success-line:`Manipulation`
    Convert the given entity class from one label to another across the
    entire Dataset.

    Args:
        original_ec (str): The entity class to change.
        modified_ec (str): The entity class to change to.
    """
    n_modified = 0
    for doc in self.documents:
        a = doc.annotation
        for m in a.mentions:
            if m.label == original_ec:
                m.label = modified_ec
                n_modified += 1
    logger.info(
        f'Convert Entity class "{original_ec}" -> "{modified_ec}": '
        f" modified {n_modified} entities."
    )


def convert_relation_class(self: Dataset, original_rc: str, modified_rc: str):
    """
    :bdg-success-line:`Manipulation`
    Convert the given relation class from one label to another across the
    entire Dataset.

    Args:
        original_ec (str): The relation class to change.
        modified_ec (str): The relation class to change to.
    """
    n_modified = 0
    for doc in self.documents:
        a = doc.annotation
        for r in a.relations:
            if r.label == original_rc:
                r.label = modified_rc
                n_modified += 1
    logger.info(
        f'Convert Relation class "{original_rc}" -> "{modified_rc}": '
        f"modified {n_modified} relations."
    )


def flatten_all_entities(self: Dataset):
    """
    :bdg-success-line:`Manipulation`
    Flatten all entities, i.e. resolve all hierarchical entities to their
    base class. For example,
    ["state/desirable"] becomes ["state"], etc.
    """
    n_modified = 0
    for doc in self.documents:
        a = doc.annotation
        for m in a.mentions:
            m.label = m.label.split("/")[0]
        n_modified += len(a.mentions)
    logger.info(
        f"Successfully flattened all {n_modified} entities in dataset."
    )


def flatten_all_relations(self: Dataset):
    """
    :bdg-success-line:`Manipulation`
    Flatten all relations, i.e. resolve all hierarchical relations to their
    base class. For example,
    ["state/desirable"] becomes ["state"], etc.
    """
    n_modified = 0
    for doc in self.documents:
        a = doc.annotation
        for r in a.relations:
            r.label = r.label.split("/")[0]
        n_modified += len(a.relations)
    logger.info(
        f"Successfully flattened all {n_modified} relations in dataset."
    )


Dataset.drop_entity_class = drop_entity_class
Dataset.drop_relation_class = drop_relation_class
Dataset.convert_entity_class = convert_entity_class
Dataset.convert_relation_class = convert_relation_class
Dataset.flatten_all_entities = flatten_all_entities
Dataset.flatten_all_relations = flatten_all_relations
