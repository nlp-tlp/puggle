.. _data-format-requirements:

Data Format Requirements
========================

Puggle's :py:meth:`~puggle.Dataset.Dataset.load_documents` function reads two types of files:

-   The first argument is the file containing the structured fields, i.e. a CSV dataset
-   The second argument is the file containing the annotations, i.e. a dictionary containing `tokens`, `entities` (or `mentions`), and `relations`.

Note that these are both optional - you can use Puggle with only an annotations file, or only a structured file, if you like.

In this section we explain the required format of the structured fields, annotations, and then discuss how they can be used together.

Structured fields
-----------------

The format required for the structured fields is straightforward. It just needs a header row and any number of body rows. For example::

    text,date,x,y
    one three two,12/05/2020,4,test
    four six five,04/05/2020,12,another

When using :py:meth:`~puggle.Dataset.Dataset.load_into_neo4j`, the structured fields will be included as properties on the Document nodes. At the moment they are stored as strings - in future we will allow for integers to be interpreted as ints, dates to be converted to dates, etc.

Annotations
-----------

The format of your annotations file (or dictionaries, if loading them in programatically in Python) must match the correct format for Puggle to be able to read them in.

Note that you shouldn't have to worry about this if you are getting the outputs directly from SPERT or QuickGraph - they should already be formatted this way, so you can simply load them into Puggle.

SPERT format
^^^^^^^^^^^^

The SPERT format is as follows:

.. code-block:: json

    [
        {
            "tokens": ["one", "three", "two"],
            "entities": [
                { "start": 0, "end": 1, "type": "number" },
                { "start": 1, "end": 2, "type": "number" },
                { "start": 2, "end": 3, "type": "number" }
            ],
            "relations": [
                { "head": 1, "tail": 0, "type": "bigger_than" },
                { "head": 1, "tail": 2, "type": "bigger_than" }
            ]
        },
    ]

QuickGraph format
^^^^^^^^^^^^^^^^^

The QuickGraph format is as follows:

.. code-block:: json

    [
        "annotator_1": [
            {
                "tokens": ["one", "three", "two"],
                "entities": [
                    { "id": "<random id 1>", "start": 0, "end": 0, "label": "number" },
                    { "id": "<random id 2>", "start": 1, "end": 1, "label": "number" },
                    { "id": "<random id 3>", "start": 2, "end": 2, "label": "number" }
                ],
                "relations": [
                    { "id": "<random id 4>", "source_id": "<random id 2>", "target_id": "<random id 1>", "label": "bigger_than" },
                    { "id": "<random id 5>", "source_id": "<random id 2>", "target_id": "<random id 3>", "label": "bigger_than" }
                ]
            },
        ],
    ]

Note that the `end` indexes are 1 lower than the `end` indexes in the SPERT output, i.e. it is the index of the token on which the entity mention ends, rather than the index of the token *after* the entity mention.

The keys are also different, i.e. entities and relations have `label` rather than type.

Also note that QuickGraph also includes some other fields in its output, but they are not used by Puggle (no need to remove them yourself).

.. warning::

    When importing annotations from Quickgraph, puggle will load the annotations of all annotators, which may result in duplicate nodes and edges. You may want to combine/compile them first before using Puggle, or only load in the annotations of one person.

"Native Puggle" format
^^^^^^^^^^^^^^^^^^^^^^

When loading documents in Puggle programatically in Python, the format for the annotations must be in "Native Puggle" format (i.e. the same way they are stored "under the hood" in Puggle). This is as follows:

.. code-block:: python

    d = {
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

This can be seen as a middleground between SPERT and QuickGraph. It notably models entity labels as a list, rather than a single string, meaning it can store multiple labels per entity.

Using Structured fields and Annotations together
------------------------------------------------

When using both a structured file and an annotations file, your structured fields (csv) and annotations (json) need to have the same number of rows. Each row in one dataset must correspond to the other. For example, row 5 of `documents.csv` should be the structured fields corresponding to the annotation in row 5 of `annotations.json`.

Typically your "annotations" would be the output of labelling one of the fields from the structured data using something like SPERT. For example, in your structured data you might have a field `short_text_description`, which might contain textual descriptions of events. Your annotations file could contain the annotated sentences from those descriptions, capturing the entities appearing within them, and the relationships between those entities.

In the example above we have used the `text` field as an example. In the structured fields file, it is the first column, containing sentences such as "one two three" and "four five six". In our annotations file, each sentence has been labelled with its corresponding entities, and the relationships between those entities. The ordering between the two files is the same, thus each annotation from row `x` of the annotations file corresponds to the same set of structured fields from row `x` of the structured fields file.