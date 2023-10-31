import pytest
from puggle import Annotation


def test_annotation_repr():
    """Simple function to just make sure an annotation prints out properly."""
    d = {
        "tokens": ["one", "two"],
        "entities": [
            {"start": 0, "end": 1, "label": "number"},
            {"start": 1, "end": 2, "label": "number"},
        ],
        "relations": [{"start": 0, "end": 1, "type": "smaller_than"}],
    }
    a = Annotation.from_dict(d)
    assert str(a).startswith("Tokens: one two\nMentions")
