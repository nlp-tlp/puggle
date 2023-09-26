# Puggle

This library is designed to provide utilities for working with the outputs of entity typing models such as [SPERT](https://github.com/lavis-nlp/spert/), [E2EET](https://github.com/Michael-Stewart-Webdev/e2e-entity-typing), etc.

## Data format

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

## Commands

To build the docs:

    poetry run pdoc3 puggle --html

TODO: try sphinx
