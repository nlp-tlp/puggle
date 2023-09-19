"""A dataset that stores tokens and labels in ET format."""
import os
import json
import random
import logging as logger
from json import JSONDecodeError
from typing import List

from .Document import Document


class Dataset(object):
    """A class representing a Dataset, which
    stores Documents in the form of Mentions and Relations.
    """

    def __init__(self, filepath):
        """Load a Dataset from a file path. The file must be .json.


        Args:
            filepath (os.path): The file path to load the dataset from.
        """
        super(Dataset, self).__init__()
        self.documents = self._load_documents_from_file(filepath)

    def save_to_file(self, filename: str):
        """Save the documents of this dataset to the given filename.

        Args:
            filename (str): The filename to save to.
        """
        with open(filename, "w") as f:
            json.dump([doc.to_dict() for doc in self.documents], f)

    def flatten(self):
        """Flatten the dataset, i.e. ensure every mention has only one
        label.
        """
        for doc in self.documents:
            doc.flatten()

    def _load_documents_from_file(self, filename: os.path):
        """Load a list of Document objects from the given file.

        Args:
            filename (str): The filename to load from.

        Returns:
            list: A list of Documents.
        """
        documents = []
        with open(filename, "r") as f:
            try:
                d = json.load(f)
                for i, doc in enumerate(d):
                    documents.append(Document.from_dict(doc, doc_idx=i))

            except (JSONDecodeError, ValueError) as e:
                raise ValueError(
                    f"The .json file ({os.path.basename(filename)}) "
                    f"failed to parse due to the following issue: {e}"
                )
        logger.debug(f"Loaded {len(documents)} documents from {filename}.")
        return documents

    def __repr__(self):
        """String representation of the dataset.

        Returns:
            str: String representation of the dataset.
        """
        return f"Dataset containing {len(self.documents)} documents."
