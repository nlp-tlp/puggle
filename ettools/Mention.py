""" A mention, which is used in the Redcoat documents."""


class Mention(object):
    """A single entity mention. Captures the start, end, tokens and
    labels of the mention."""

    def __init__(
        self,
        start: int,
        end: int,
        tokens: list,
        labels: list,
        mention_id: int,
    ):
        super(Mention, self).__init__()
        self.start = start
        self.end = end
        self.tokens = tokens
        self.labels = labels
        self.mention_id = mention_id

    def get_first_label(self):
        """A simple function to retrieve the first label of a mention.

        Args:
            mention (dict): The mention to get the first label of.

        Returns:
            str: The first label, e.g. "Item".
        """
        labels = self.labels
        all_labels = [x for x in labels]
        first_label = all_labels[0] if len(all_labels) > 0 else None
        return first_label

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        if len(self.labels) == 1:
            return f"({' '.join(self.tokens)} [{self.labels[0]}])"
        else:
            return f"({' '.join(self.tokens)} {self.labels})"
