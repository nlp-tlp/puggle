from puggle import Dataset


def count_unique_tokens(dataset: Dataset):
    """Return the number of unique tokens in the given Dataset.

    Args:
        dataset (Dataset): The dataset to check.

    Returns:
        int: The number of unique tokens in the dataset.
    """

    seen_tokens = set()
    for d in dataset.documents:
        for token in d.annotation.tokens:
            seen_tokens.add(token)

    return len(list(seen_tokens))
