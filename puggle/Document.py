"""A class representing a single Document.
Contains an optional Annotation, and a list of fields."""

from typing import List, Dict

from .Annotation import Annotation


class Document(object):

    """A class representing a single Document.
    Contains an optional Annotation, and a list of fields.
    """

    def __init__(self, doc_idx: int):
        super(Document, self).__init__()
        self.doc_idx = doc_idx
        self.fields = None
        self.annotation = None

    def add_annotation(self, annotation: Annotation):
        """Add the given annotation to this Document.

        Args:
            annotation (Annotation): An annotation.
        """
        self.annotation = annotation

    def add_fields(self, fields: List[Dict]):
        """Add the given list of fields (each of which are
        key: value pairs) to this Document.

        Args:
            fields (List[Dict]): List of fields.
        """
        self.fields = fields

    def to_dict(self):
        return {
            "doc_idx": self.doc_idx,
            "fields": self.fields,
            "annotations": self.annotation.to_dict()
            if self.annotation
            else None,
        }
