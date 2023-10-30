"""Tools for manipulating Puggle datasets. When this library is imported,
the functions will be added to the Dataset class."""
from puggle import Dataset


def drop_entity_class(self: Dataset, entity_class: str):
    """Remove any instances of the given entity class from the mentions of the
    given Dataset.
    Also remove all Relations referencing the deleted mentions.

    Args:
        dataset (Dataset): The dataset to manipulate.
        entity_class (str): The entity class to remove.
    """
    dataset = self
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


def drop_relation_class(self: Dataset, relation_class: str):
    """Remove any instances of the given relation class from the relations of
    the given Dataset.

    Args:
        dataset (Dataset): The dataset to manipulate.
        relation_class (str): The relation class to remove.
    """
    dataset = self
    for doc in dataset.documents:
        a = doc.annotation
        a.relations = list(
            filter(lambda r: r.label != relation_class, a.relations)
        )


Dataset.drop_entity_class = drop_entity_class
Dataset.drop_relation_class = drop_relation_class
