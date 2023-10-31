import pytest
from puggle import Document, Annotation


@pytest.mark.parametrize(
    "annotation, structured_fields",
    [
        (
            {
                "tokens": ["one", "two"],
                "entities": [
                    {"start": 0, "end": 1, "label": "number"},
                    {"start": 1, "end": 2, "label": "number"},
                ],
                "relations": [],
            },
            {"test": 5},
        ),
        (
            {
                "tokens": ["one", "two"],
                "entities": [
                    {"start": 0, "end": 1, "label": "number"},
                    {"start": 1, "end": 2, "label": "number"},
                ],
                "relations": [{"start": 0, "end": 1, "type": "test"}],
            },
            None,
        ),
    ],
)
def test_document_to_string(annotation, structured_fields):
    """Simple function to just make sure a Document prints out properly
    when the str() function is called. Not checking every single detail as
    it seems a bit pointless - just making sure it contains the main important
    things i.e. fields, mentions, relations etc."""
    a = Annotation.from_dict(annotation)

    d = Document(structured_fields, a)

    s = str(d)

    assert (
        "fields" in s and "mentions" in s and "relations" in s and len(s) > 20
    )
