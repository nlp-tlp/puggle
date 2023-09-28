# Puggle

This library is designed to provide utilities for working with the outputs of entity typing models such as [SPERT](https://github.com/lavis-nlp/spert/), [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing), or annotation tools such as [Quickgraph](https://quickgraph.tech/). Puggle has three main purposes:

-   Provide easy parsing of the output (i.e. annotations) of entity typing models
-   Enable the connection between structured data (csv) and those annotations
-   Provide functionality to easily load the structured data + annotations into a Neo4j graph

We do not include any code for actually running machine learning models here. Puggle is purely designed for loading the results of such models into Python-based classes and then easily importing the data into Neo4j.

Full documentation available on [ReadtheDocs](https://puggle.readthedocs.io/en/latest/).

## Installation

You can install this package via poetry:

    pip install poetry
    poetry install

It is also available on PyPI ([link](https://pypi.org/project/puggle/)), so rather than cloning this repo, you can install it via pip:

    pip install puggle

To be able to use the `load_into_neo4j` function from the `Dataset` class, you will need to have Neo4j installed and running on your machine. The easiest way to do this is via Docker, though in the interest of keeping this package light we do not include a dockerfile here.

To use the `load_into_neo4j` function you also need to set an environment variable for your Neo4j password. You can do this by creating an empty `.env` file in the root directory of this repository and including:

    NEO4J_PASSWORD=<your neo4j password>

## Basic functionality

### Loading structured data and annotations from files

Here is an example of loading in a set of annotations from a machine learning model, and combining those annotations with a structured CSV dataset.

First, import puggle and create an empty `Dataset`:

    from puggle import Dataset
    d = Dataset()

Then you can use the `load_documents` function to load a list of documents from a CSV file and a JSON file. Your structured data should be stored in the csv, and your annotations (e.g. the output of a machine learning model such as SPERT) should be stored in the JSON file.

    d.load_documents(
        sd_filename="sample_data/documents.csv",
        anns_filename="sample_data/annotations.json",
        anns_format="spert",
    )

Valid `anns_format` options are currently `quickgraph` and `spert`. Specifying a format is necessary because each of these formats differ slightly - for example, Quickgraph stores relationships differently, and uses a `label` key for its relations rather than `type`.

> Note: When importing annotations from Quickgraph, puggle will load the annotations of all annotators, which may result in duplicate nodes and edges. You may want to combine/compile them first before using Puggle, or only load in the annotations of one person.

### Creating documents programatically

You can also create a dataset and populate it programatically. Here is an example of creating the same Dataset as above, but fully in Python.

Note that your data will need to adhere to the format below. At this stage the ability to read either `quickgraph` or `spert` formats are limited to the `load_documents` function.

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

### Loading your data into Neo4j automatically

Once they are loaded, you can use the `load_into_neo4j` function to automatically create a Neo4j graph:

    d.load_into_neo4j(recreate=True)

The `recreate=True` causes the graph to be recreated from scratch.

You can then open up the Neo4j browser and write queries over your documents/entities/relationships. For example, here is what it looks like when running `MATCH (n) RETURN n` on the sample data:

![image of the graph](https://github.com/nlp-tlp/puggle/blob/main/graph.png?raw=true)

### Further documentation

For full documentation see the [ReadtheDocs](https://puggle.readthedocs.io/en/latest/).

## How does my data need to be formatted to use Puggle?

Puggle's `Document.load_documents()` function reads two types of files:

-   The first argument is the file containing the structured fields, i.e. a CSV dataset
-   The second argument is the file containing the annotations, i.e. a dictionary containing `tokens`, `entities` (or `mentions`), and `relations`.

Your structured fields (csv) and annotations (json) need to have the same number of rows. Each row in one dataset must correspond to the other. For example, row 5 of `documents.csv` should be the structured fields corresponding to the annotation in row 5 of `annotations.json`.

Typically your "annotations" would be the output of labelling one of the fields from the structured data using something like SPERT. For example, in your structured data you might have a field `short_text_description`, which might contain textual descriptions of events. Your annotations file could contain the annotated sentences from those descriptions, capturing the entities appearing within them, and the relationships between those entities.

In the example below we have used the `text` field as an example. In the structured fields file, it is the first column, containing sentences such as "one two three" and "four five six". In our annotations file, each sentence has been labelled with its corresponding entities, and the relationships between those entities. The ordering between the two files is the same, thus each annotation from row `x` of the annotations file corresponds to the same set of structured fields from row `x` of the structured fields file.

### Structured fields

The format required for the structured fields is straightforward. It just needs a header row and any number of body rows. For example:

    text,date,x,y
    one three two,12/05/2020,4,test
    four six five,04/05/2020,12,another

When using `load_into_neo4j`, the structured fields will be included as properties on the Document nodes.

### Annotations

The format for the annotations must be as follows:

    {
        "tokens": ["one", "three", "two"],
        "mentions": [
            { "start": 0, "end": 1, "labels": ["number"] },
            { "start": 1, "end": 2, "labels": ["number"] },
            { "start": 2, "end": 3, "labels": ["number"] }
        ],
        "relations": [
            { "start": 1, "end": 0, "type": "bigger_than" },
            { "start": 1, "end": 2, "type": "bigger_than" }
        ]
    }

This output follows the same format as many modern entity typing/information extraction models such as [SPERT](https://github.com/lavis-nlp/spert/) and [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing). It is also compatible with [Quickgraph](https://quickgraph.tech/).

## Why is it called Puggle?

This is a super lightweight version of [Echidna](https://github.com/nlp-tlp/mwo2kg-and-echidna), our software application for constructing knowledge graphs from unstructured text. A puggle is a baby Echidna, so it seemed appropriate!

It also works as an acronym!

Puggle = Python Utilities for Generating Graphs from Linked Entities

## TODO

-   Automatic parsing of dates, floats, etc, when building the Neo4j graph
-   A function in the `Dataset` class (`create_neo4j_csvs()`) to create CSVs to import into Neo4j, so that they can be created and then imported later/elsewhere
-   Unit tests
