""" A relation, which captures the relationship between one
:class:`~puggle.Annotation.Mention` and another. It is stored by the
:class:`~puggle.Annotation.Annotation` class."""
from .Mention import Mention


class Relation:
    """A single relation. Captures the start mention, end mention, tokens and
    labels of the relation."""

    def __init__(self, start: Mention, end: Mention, label: str):
        """Create a new Relation.

        Args:
            start (Mention): The start (head) Mention.
            end (Mention): The end (tail) Mention.
            label (str): The label (type) of the relation.

        Raises:
            ValueError: If the start and end Mention is the same.
        """
        super().__init__()

        if start == end:
            raise ValueError(
                "Cannot create relation between a mention and itself"
            )

        self.start = start
        self.end = end
        self.label = label

    def to_dict(self):
        """Return a dictionary representation of this Relation.
        Convert 'start' and 'end' to the mention index of this
        relation's start and end mention.

        Returns:
            dict: Dictionary representation of this Relation.
        """
        return {
            "start": self.start.mention_id,
            "end": self.end.mention_id,
            "type": self.label,
        }

    def __repr__(self):
        return (
            f"({' '.join(self.start.tokens)})-"
            f"[{self.label}]->({' '.join(self.end.tokens)})"
        )
