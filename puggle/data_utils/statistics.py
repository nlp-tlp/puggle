"""Statistics-based functions for the Dataset class."""
from puggle import Dataset


def get_unique_tokens_count(self: Dataset):
    """
    :bdg-danger-line:`Statistics`
    Return the number of unique tokens in this Dataset.

    Args:
        dataset (Dataset): The dataset to use.

    Returns:
        int: The number of unique tokens in the dataset.
    """

    seen_tokens = set()
    for d in self.documents:
        for token in d.annotation.tokens:
            seen_tokens.add(token)

    return len(list(seen_tokens))


def get_entity_label_counts(self: Dataset, document_level=False):
    """
    :bdg-danger-line:`Statistics`
    Return a sorted list of (entity_label, freq) pairs in this Dataset.
    The frequency is the number of times that entity_label has been used.

    Args:
        document_level (bool, optional): If True, the counts will be the
           number of documents in which the entity label appears, rather than
           the total frequency of that entity label.

    Returns:
        list[tuple]: A sorted list of (entity_label, freq) pairs.
    """
    counts_dict = {}
    for d in self.documents:
        seen_this_doc = set()
        for m in d.annotation.mentions:
            label = m.label
            if label not in counts_dict:
                counts_dict[label] = 0
            if label not in seen_this_doc or not document_level:
                counts_dict[label] += 1
            seen_this_doc.add(label)

    sorted_counts = sorted(
        counts_dict.items(), key=lambda x: x[1], reverse=True
    )

    return sorted_counts


Dataset.get_unique_tokens_count = get_unique_tokens_count
Dataset.get_entity_label_counts = get_entity_label_counts
