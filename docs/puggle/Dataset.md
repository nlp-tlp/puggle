Module puggle.Dataset
=====================
A dataset that stores tokens and labels in ET format.

Classes
-------

`Dataset(filepath)`
:   A class representing a Dataset, which
    stores Documents in the form of Mentions and Relations.
    
    Load a Dataset from a file path. The file must be .json.
    
    
    Args:
        filepath (os.path): The file path to load the dataset from.

    ### Methods

    `flatten(self)`
    :   Flatten the dataset, i.e. ensure every mention has only one
        label.

    `load_into_neo4j(self, recreate=False)`
    :   Load the Dataset into a Neo4j database.
        Automatically creates Nodes from the entities (mentions) appearing
        in each document, and relationships between them via the Relations.
        
        Raises:
            RuntimeError: If the Neo4j server is not running.
        
        Args:
            recreate (bool, optional): If true, the Neo4j db will be
               cleared prior to inserting the documents into it.

    `save_to_file(self, filename: str)`
    :   Save the documents of this dataset to the given filename.
        
        Args:
            filename (str): The filename to save to.