Module puggle.Relation
======================
A relation, which is used in the Redcoat documents.

Classes
-------

`Relation(start: puggle.Mention.Mention, end: puggle.Mention.Mention, label: str)`
:   A single relation. Captures the start mention, end mention, tokens and
    labels of the relation.

    ### Methods

    `to_dict(self)`
    :   Return a dictionary representation of this Relation.
        Convert 'start' and 'end' to the mention index of this
        relation's start and end mention.
        
        Returns:
            dict: Dictionary representation of this Relation.