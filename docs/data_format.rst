Data Format Requirements
========================

Puggle's `Document.load_documents()` function reads two types of files:

-   The first argument is the file containing the structured fields, i.e. a CSV dataset
-   The second argument is the file containing the annotations, i.e. a dictionary containing `tokens`, `entities` (or `mentions`), and `relations`.

Your structured fields (csv) and annotations (json) need to have the same number of rows. Each row in one dataset must correspond to the other. For example, row 5 of `documents.csv` should be the structured fields corresponding to the annotation in row 5 of `annotations.json`.

Typically your "annotations" would be the output of labelling one of the fields from the structured data using something like SPERT. For example, in your structured data you might have a field `short_text_description`, which might contain textual descriptions of events. Your annotations file could contain the annotated sentences from those descriptions, capturing the entities appearing within them, and the relationships between those entities.

In the example below we have used the `text` field as an example. In the structured fields file, it is the first column, containing sentences such as "one two three" and "four five six". In our annotations file, each sentence has been labelled with its corresponding entities, and the relationships between those entities. The ordering between the two files is the same, thus each annotation from row `x` of the annotations file corresponds to the same set of structured fields from row `x` of the structured fields file.

Structured fields
-----------------

The format required for the structured fields is straightforward. It just needs a header row and any number of body rows. For example::

    text,date,x,y
    one three two,12/05/2020,4,test
    four six five,04/05/2020,12,another

When using `load_into_neo4j`, the structured fields will be included as properties on the Document nodes.

Annotations
-----------

The format for the annotations must be as follows:

.. code-block:: json

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

This output follows the same format as many modern entity typing/information extraction models such as `SPERT <https://github.com/lavis-nlp/spert/>`_ and `E2EET <https://github.com/Michael-Stewart-Webdev/e2e-entity-typing>`_. It is also compatible with `Quickgraph <https://quickgraph.tech/>`_.