import random
from puggle import Dataset, Annotation, Document


def smart_sample(
    dataset: Dataset, num_records: int, num_samples: int
) -> Dataset:
    """Run a 'smart sample' on the given dataset to return a new Dataset with
    num_records documents.
    Repeat the sampling process num_samples times and select the best
    example.

    Args:
        dataset (Dataset): The dataset to sample.
        num_records (int): The number of documents that should appear in the
           output.
        num_samples (int): Number of times to repeat the process.
    """
    documents = dataset.documents

    # Repeat num_samples times to create a list of num_samples different
    # 'sample sets'. The best of these will be chosen as the final output.
    sample_sets = []
    for sample_index in range(num_samples):
        # Begin by selecting a random document.
        start_doc = random.choice(documents)
        sample_set = [start_doc]

        # For num_records - 1 times, calculate the scores of each document
        # against the current sample set in this iteration.
        # This will initially be just one document (the randomly selected
        # one from earlier), and will be iteratively built up 1 document
        # at a time.
        for x in range(num_records - 1):
            scored_documents = []
            for doc in documents:
                if doc in sample_set:
                    continue

                # Use the scoring function to determine the score of this
                # document. Lower scores are better (less similarity).
                score = _calculate_document_score(doc, sample_set)
                scored_documents.append((doc, score))

            scored_documents.sort(key=lambda x: x[1])
            sample_set.append(scored_documents[0][0])

        # Now that we have num_samples documents in the sample set,
        # calculate the average score of every document in that set against
        # every other document in the set.
        # The average score determines how 'good' our sample set is.
        average_score = sum(
            [_calculate_document_score(doc, sample_set) for doc in sample_set]
        ) / len(sample_set)

        sample_sets.append((sample_set, average_score))

    output_dataset = Dataset()

    # Sort these sample sets, taking the one with the highest score as the
    # final output dataset.
    sample_sets.sort(key=lambda x: x[1], reverse=True)
    print(f"Average scores of each of the {num_samples} sample sets:")
    for docs, score in sample_sets:
        print(score)

    print("Creating final output dataset from the highest-scored sample...")
    for d in sample_sets[0][0]:
        output_dataset.add_document(d)

    return output_dataset


def _calculate_document_score(document: Document, sample_set: list[Document]):
    """Calculate the 'score' of the given document by comparing it
    to every document in the sample set so far.

    Args:
        document (Document): The document to calculate the score of.
        sample_set (Dataset): The current sample set.

    Returns:
        float: The total score.
    """
    token_score = 0
    entity_score = 0
    relation_score = 0

    # Token score
    token_scores = []
    for t in document.annotation.tokens:
        freq = 0
        for other_doc in sample_set:
            if t in other_doc.annotation.tokens:
                freq += 1
        ts = freq / len(sample_set)
        token_scores.append(ts)
    token_score = sum(token_scores) / len(token_scores)

    return (token_score + entity_score + relation_score) / 3
