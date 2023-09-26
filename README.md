# Puggle

This library is designed to provide utilities for working with the outputs of entity typing models such as [SPERT](https://github.com/lavis-nlp/spert/), [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing), etc. It has three main purposes:

    - Provide easy parsing of the output (i.e. annotations) of entity typing models
    - Enable the connection between structured data (csv) and those annotations
    - Provide functionality to easily load the structured data + annotations into a Neo4j graph

## Running the code

You can install this package via poetry:

    pip install poetry
    poetry install

We plan to release it on PyPI soon.

## Basic functionality

At the moment the functionality is quite basic. Here is an example of loading in a set of annotations from a machine learning model, combining those annotations with a structured dataset, and then loading it all into Neo4j.

    from puggle import Dataset

    d = Dataset()
    d.load_documents("sample_data/documents.csv", "sample_data/annotations.json")

    d.load_into_neo4j(recreate=True)

For this to work, your `documents.csv` and `annotations.json` need to have the same number of rows. Each row in one dataset must correspond to the other. For example, row 5 of `documents.csv` should be the structured fields corresponding to the annotation in row 5 of `annotations.json`.

## How does my data need to be formatted to use Puggle?

Puggle reads two types of files:

-   Structured fields, i.e. CSV datasets
-   Annotations, i.e. a dictionary containing `tokens`, `entities` (or `mentions`), and `relations`.

### Structured fields

The format required for the structured fields is straightforward. It just needs a header row and any number of body rows. For example:

    text,date,x,y
    one three two,12/05/2020,4,test
    four six five,04/05/2020,12,another

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
