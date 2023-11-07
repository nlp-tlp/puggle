""" A mention, which is stored by the :class:`~puggle.Annotation.Annotation`
class."""


class Mention:
    """A single entity mention. Captures the start, end, tokens and
    labels of the mention."""

    def __init__(
        self,
        start: int,
        end: int,
        tokens: list,
        label: str,
        mention_id: int,
    ):
        """Create a new Mention.

        Args:
            start (int): The index of the first token of the mention.
            end (int): The index of the last token of the mention.
            tokens (list): The list of tokens appearing in the mention.
            label (str): The label of the mention.
            mention_id (int): The index of this mention with respect to the
               Document in which it appears.
        """
        super().__init__()
        if start == end:
            raise ValueError(
                "Mention start index cannot be the same as its end index."
            )
        self.start = start
        self.end = end
        self.tokens = tokens
        self.label = label
        self.mention_id = mention_id

    def to_dict(self):
        """Return a dictionary representation of this mention.
        Don't include the mention_id as it is not useful here - it is only
        used when creating Relation objects between Mentions.

        Returns:
            dict: The mention as a dictionary.
        """
        return {k: v for k, v in self.__dict__.items() if k != "mention_id"}

    def __repr__(self):
        return f"({' '.join(self.tokens)} [{self.label}]) (start: {self.start}, end: {self.end})"
