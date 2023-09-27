"""A class representing a single Document.
Contains an optional Annotation, and a list of fields."""

from typing import List, Dict

from .Annotation import Annotation


class Document(object):

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
        super(Document, self).__init__()
        self.fields = structured_fields
        self.annotation = annotation

    def set_annotation(self, annotation: Annotation):
        """Set this Document's Annotation to the given Annotation.

        Args:
            annotation (Annotation): An annotation.
        """
        self.annotation = annotation

    def set_fields(self, fields: List[Dict]):
        """Set this Document's structured fields (each of which are
        key: value pairs) to the given list of dicts.

        Args:
            fields (List[Dict]): List of fields.
        """
        self.fields = fields

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
