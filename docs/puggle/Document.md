Module puggle.Document
======================
A class that stores documents in Mention format.

Classes
-------

`Document(doc_idx: int, tokens: list, mentions: list, relations: list = None)`
:   A Document. Contains a single document index, a list of
    tokens, a list of mentions, a list of relations.
    
    Create a new Document.
    
    Args:
        doc_idx (int): The index of the document in the dataset.
        tokens (list): The list of tokens of the document.
        mentions (list): The list of mentions of the document. Each
           mention must follow the correct format ('start', 'end',
           'mentions'/'entities', 'labels'/'type').
        relations (list, optional): The list of relations of the
           document. Each relation must follow the correct format
           ('start'/'head', 'end'/'tail', 'type').

    ### Static methods

    `from_dict(d: dict, doc_idx: int)`
    :   Create a Document from a dictionary and doc_idx.
        
        Args:
            d (dict): The dictionary. Must contain doc_idx,
            tokens, mentions, relations.
            doc_idx (int): The document index.
        
        Returns:
            Document: A Document.
        
        Raises:
            ValueError: If the dictionary is missing a required
            key.

    ### Methods

    `flatten(self)`
    :   Flatten this doc, i.e. ensure each mention only has one label.

    `to_dict(self)`
    :   Return a dictionary representation of this Document.
        Format will be similar to the input dataset.
        
        Returns:
            dict: Dictionary representation of this Document.