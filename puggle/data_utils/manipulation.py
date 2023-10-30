"""Tools for manipulating Puggle datasets. When this library is imported,
the functions will be added to the Dataset class."""
from puggle import Dataset
from puggle.logger import logger


def drop_entity_class(self: Dataset, entity_class: str):
    """Remove any instances of the given entity class from the mentions of the
    given Dataset.
    Also remove all Relations referencing the deleted mentions.

    Args:
        dataset (Dataset): The dataset to manipulate.
        entity_class (str): The entity class to remove.
    """
    dataset = self
    n_removed_e = 0
    n_removed_r = 0
    for doc in dataset.documents:
        a = doc.annotation

        a.mentions = list(
            filter(lambda m: m.get_first_label() != entity_class, a.mentions)
        )
        a.relations = list(
            filter(
                lambda r: ((r.start in a.mentions) or (r.end in a.mentions)),
                a.relations,
            )
        )
    logger.info(
        f'Drop Entity class "{entity_class}": removed {n_removed_e} entities '
        f"and {n_removed_r} connected relations."
    )


def drop_relation_class(self: Dataset, relation_class: str):
    """Remove any instances of the given relation class from the relations of
    the given Dataset.

    Args:
        dataset (Dataset): The dataset to manipulate.
        relation_class (str): The relation class to remove.
    """
    dataset = self
    n_removed = 0
    for doc in dataset.documents:
        a = doc.annotation
        n_removed += sum([r.label == relation_class for r in a.relations])
        a.relations = list(
            filter(lambda r: r.label != relation_class, a.relations)
        )

    logger.info(
        f'Drop Relation class "{relation_class}": removed {n_removed} relations.'
    )


def convert_entity_class(self: Dataset, original_ec: str, modified_ec: str):
    """Convert the given entity class from one label to another.

    Args:
        original_ec (str): The entity class to change.
        modified_ec (str): The entity class to change to.
    """
    n_modified = 0
    for doc in self.documents:
        a = doc.annotation
        for m in a.mentions:
            if m.get_first_label() == original_ec:
                m.labels[0] = modified_ec
                n_modified += 1
    logger.info(
        f'Convert Entity class "{original_ec}" -> "{modified_ec}": '
        f" modified {n_modified} entities."
    )


def convert_relation_class(self: Dataset, original_rc: str, modified_rc: str):
    """Convert the given relation class from one label to another.

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
    """Flatten all entities, i.e. resolve all hierarchical entities to their
    base class, and remove all but the first label. For example,
    ["state/desirable"] becomes ["state"], etc.
    """
    for doc in self.documents:
        a = doc.annotation
        for m in a.mentions:
            m.labels = [m.get_first_label().split("/")[0]]
    logger.info("Successfully flattened all entities in dataset.")


Dataset.drop_entity_class = drop_entity_class
Dataset.drop_relation_class = drop_relation_class
Dataset.convert_entity_class = convert_entity_class
Dataset.convert_relation_class = convert_relation_class
Dataset.flatten_all_entities = flatten_all_entities
