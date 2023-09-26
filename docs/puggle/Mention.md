Module puggle.Mention
=====================
A mention, which is used in the Redcoat documents.

Classes
-------

`Mention(start: int, end: int, tokens: list, labels: list, mention_id: int)`
:   A single entity mention. Captures the start, end, tokens and
    labels of the mention.

    ### Methods

    `get_first_label(self)`
    :   A simple function to retrieve the first label of a mention.
        
        Args:
            mention (dict): The mention to get the first label of.
        
        Returns:
            str: The first label, e.g. "Item".

    `to_dict(self)`
    :