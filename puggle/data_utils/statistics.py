from puggle import Dataset


def count_unique_tokens(self: Dataset):
    """Return the number of unique tokens in the given Dataset.

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
    """Return a sorted list of (entity_label, freq) pairs.
    The frequency is the number of times that entity_label has been used.

    Args:
        dataset (Dataset): The dataset to use.
        document_level (bool, optional): If True, the counts will be the
           number of documents in which the entity label appears, rather than
           the total frequency of that entity label.

    Returns:
        list[tuple]: A sorted list of (entity_label, freq) pairs.
    """
    counts_dict = {}
    counts = []
    for d in self.documents:
        for m in d.annotation.mentions:
            label = m.get_first_label()
            if label not in counts_dict:
                counts_dict[label] = 0
            counts_dict[label] += 1
            if document_level:
                break

    sorted_counts = sorted(
        counts_dict.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_counts


Dataset.count_unique_tokens = count_unique_tokens
Dataset.get_entity_label_counts = get_entity_label_counts
