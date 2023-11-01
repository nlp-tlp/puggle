"""A class representing a single Document.
Contains an optional Annotation, and a list of fields."""

from typing import List, Dict

from .Annotation import Annotation


class Document:

    """A class representing a single Document.
    Contains an optional Annotation, and a list of fields.
    """

    def __init__(
        self,
        structured_fields: List[Dict] = None,
        annotation: Annotation = None,
    ):
        """Create a new document.

        Args:
            structured_fields (List[Dict], optional): List of fields.
            annotation (Annotation, optional): The Annotation of the textual
               part of this document (such as annotations over the short text)
        """
        super().__init__()
        self.fields = structured_fields
        self.annotation = annotation

    def to_dict(self):
        """Return a dict of this Document.

        Returns:
            dict: A dictionary representing this document.
        """
        return {
            "fields": self.fields,
            "annotations": self.annotation.to_dict()
            if self.annotation
            else None,
        }

    def __str__(self):
        return str(self.to_dict())
