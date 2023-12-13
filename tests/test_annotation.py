import pytest
from puggle import Annotation


def test_annotation_repr():
    """Test that an Annotation is created correctly from a dictionary."""
    d = {
        "tokens": ["one", "two"],
        "entities": [
            {"start": 0, "end": 1, "label": "number"},
            {"start": 1, "end": 2, "label": "number"},
        ],
        "relations": [{"start": 0, "end": 1, "type": "smaller_than"}],
    }
    a = Annotation.from_dict(d)

    # Check for correct tokens and quantities of tokens
    assert len(a.tokens) == 2
    assert a.tokens == ["one", "two"]

    # Check for correct entities and quantities of entities
    assert len(a.mentions) == 2
    assert a.mentions[0].start == 0
    assert a.mentions[0].end == 1
    assert a.mentions[0].label == "number"
    assert a.mentions[0].tokens == ["one"]
    assert a.mentions[0].mention_id == 0
    
    assert a.mentions[1].start == 1
    assert a.mentions[1].end == 2
    assert a.mentions[1].tokens == ["two"]
    assert a.mentions[1].label == "number"
    assert a.mentions[1].mention_id == 1

    # Check for correct relations and quantities of relations
    assert len(a.relations) == 1
    assert a.relations[0].start == a.mentions[0]
    assert a.relations[0].end == a.mentions[1]
    assert a.relations[0].label == "smaller_than"

    # Check for correct string representation
    assert str(a).startswith("Tokens: one two\nMentions")

def test_invalid_dictionary():
    """Test exception handling for incorrect dictionary format."""
    empty_dict = {}
    missing_tokens = {"entities": [], "relations": []}
    missing_entities = {"tokens": [], "relations": []}
    missing_relations = {"tokens": [], "entities": []}

    # Test 1: Empty dictionary
    with pytest.raises(ValueError) as e:
        a = Annotation.from_dict(empty_dict)
    assert str(e.value) == "Dictionary must contain tokens, entities, and relations."

    # Test 2: Missing 'tokens' key
    with pytest.raises(ValueError) as e:
        a = Annotation.from_dict(missing_tokens)
    assert str(e.value) == "Dictionary must contain tokens, entities, and relations."

    # Test 3: Missing 'entities' key
    with pytest.raises(ValueError) as e:
        a = Annotation.from_dict(missing_entities)
    assert str(e.value) == "Dictionary must contain tokens, entities, and relations."

    # Test 4: Missing 'relations' key
    with pytest.raises(ValueError) as e:
        a = Annotation.from_dict(missing_relations)
    assert str(e.value) == "Dictionary must contain tokens, entities, and relations."