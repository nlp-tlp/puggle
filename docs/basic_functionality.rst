Basic Functionality
===================

Loading structured data and annotations from files
--------------------------------------------------

Here is an example of loading in a set of annotations from a machine learning model, and combining those annotations with a structured CSV dataset.

First, import puggle and create an empty `Dataset`:

.. code-block:: python

   from puggle import Dataset
   d = Dataset()

Then you can use the `load_documents` function to load a list of documents from a CSV file and a JSON file. Your structured data should be stored in the csv, and your annotations (e.g. the output of a machine learning model such as SPERT) should be stored in the JSON file.

.. code-block:: python

    d.load_documents(
        sd_filename="sample_data/documents.csv",
        anns_filename="sample_data/annotations.json",
        anns_format="spert",
    )

Valid `anns_format` options are currently `quickgraph` and `spert`. Specifying a format is necessary because each of these formats differ slightly - for example, Quickgraph stores relationships differently, and uses a `label` key for its relations rather than `type`.

Creating documents programatically
----------------------------------

You can also create a dataset and populate it programatically. Here is an example of creating the same Dataset as above, but fully in Python.

Note that your data will need to adhere to the format below. At this stage the ability to read either `quickgraph` or `spert` formats are limited to the `load_documents` function.

.. code-block:: python

    from puggle import Dataset, Document, Annotation

    d = Dataset()

    f1 = {"text": "one three two", "date": "12/05/2020", "x": "4", "y": "test"}
    a1 = Annotation.from_dict(
        {
            "tokens": ["one", "three", "two"],
            "entities": [
                {"start": 0, "end": 1, "labels": ["number"]},
                {"start": 1, "end": 2, "labels": ["number"]},
                {"start": 2, "end": 3, "labels": ["number"]},
            ],
            "relations": [
                {"start": 1, "end": 0, "type": "bigger_than"},
                {"start": 1, "end": 2, "type": "bigger_than"},
            ],
        }
    )

    doc1 = Document(f1, a1)
    d.add_document(doc1)

    f2 = {"text": "four six five", "date": "04/05/2020", "x": "12", "y": "another"}
    a2 = Annotation.from_dict(
        {
            "tokens": ["four", "six", "five"],
            "entities": [
                {"start": 0, "end": 1, "labels": ["number"]},
                {"start": 1, "end": 2, "labels": ["number"]},
                {"start": 2, "end": 3, "labels": ["number"]},
            ],
            "relations": [
                {"start": 1, "end": 0, "type": "bigger_than"},
                {"start": 1, "end": 2, "type": "bigger_than"},
            ],
        }
    )

    doc2 = Document(f2, a2)
    d.add_document(doc2)

Note that we call the `from_dict` function in the `Annotation` class to convert the dictionary into an Annotation object. We can then include the fields (dictionary) and this Annotation object as arguments to the constructor of the `Document` class, then add this newly-created `Document` object to our dataset.

Loading your data into Neo4j automatically
------------------------------------------

Once they are loaded, you can use the `load_into_neo4j` function to automatically create a Neo4j graph:

.. code-block:: python

   d.load_into_neo4j(recreate=True)

The `recreate=True` causes the graph to be recreated from scratch.

You can then open up the Neo4j browser and write queries over your documents/entities/relationships. For example, here is what it looks like when running `MATCH (n) RETURN n` on the sample data:

.. image:: ../graph.png
   :alt: An image of the graph.
