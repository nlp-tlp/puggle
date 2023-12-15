import pytest


# Test drop entity class
@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("small", "number", "small_after_drop_ec"),         # drop number class
        ("medium", "number", "medium_after_drop_ec"),       # drop number class
        ("large", "animal", "large_after_drop_ec"),         # drop animal class
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_entity_class(dataset, drop_class, dataset_after):
    dataset.drop_entity_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("empty", "x", "empty"),        # x class doesn't exist
        ("small", "noise", "small"),    # noise class doesn't exist
        ("medium", "fruit", "medium"),  # fruit class doesn't exist
        ("large", "number", "large"),   # number class doesn't exist
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_missing_entity_class(dataset, drop_class, dataset_after):
    dataset.drop_entity_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


# Test drop relation class
@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("small", "bigger_than", "small_after_drop_rc"),    # drop bigger_than class
        ("medium", "sounds_like", "medium_after_drop_rc"),  # drop sounds_like class
        ("large", "similar_to", "large_after_drop_rc"),     # drop similar_to class
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_relation_class(dataset, drop_class, dataset_after):
    dataset.drop_relation_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, drop_class, dataset_after",
    [
        ("empty", "x", "empty"),            # x class doesn't exist
        ("small", "sounds_like", "small"),  # sounds_like class doesn't exist
        ("medium", "similar_to", "medium"), # similar_to class doesn't exist
        ("large", "bigger_than", "large"),  # bigger_than class doesn't exist
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_drop_missing_relation_class(dataset, drop_class, dataset_after):
    dataset.drop_relation_class(drop_class)
    assert dataset.to_list() == dataset_after.to_list()


# Test convert entity class
@pytest.mark.parametrize(
    "dataset, class_from, class_to, dataset_after",
    [
        ("small", "number", "pingu", "small_after_convert_ec"),             # convert number to pingu
        ("medium", "noise", "pingu", "medium_after_convert_ec"),            # convert noise to pingu
        ("medium", "noise", "noise", "medium"),                             # convert to itself
        ("large", "celestial/sun", "planet", "large_after_convert_ec_1"),   # convert celestial/sun to planet
        ("large", "animal", "mammal", "large_after_convert_ec_2"),          # convert animal to mammal
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_convert_entity_class(
    dataset, class_from, class_to, dataset_after
):
    dataset.convert_entity_class(class_from, class_to)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, class_from, class_to, dataset_after",
    [
        ("empty", "none", "nothing", "empty"),      # none class doesn't exist
        ("small", "none", "pingu", "small"),        # none class doesn't exist
        ("large", "none", "planet", "large"),       # none class doesn't exist
        ("large", "CELESTIAL", "planet", "large"),  # case sensitive
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_convert_missing_entity_class(
    dataset, class_from, class_to, dataset_after
):
    dataset.convert_entity_class(class_from, class_to)
    assert dataset.to_list() == dataset_after.to_list()
    

# Test convert relation class
@pytest.mark.parametrize(
    "dataset, class_from, class_to, dataset_after",
    [
        ("small", "bigger_than", "bigger_than", "small"),                   # convert to itself
        ("small", "bigger_than", "pingu", "small_after_convert_rc"),        # convert bigger_than to pingu
        ("medium", "bigger_than", "pingu", "medium_after_convert_rc"),      # convert bigger_than to pingu      
        ("large", "similar_to", "comparable_to", "large_after_convert_rc"), # convert similar_to to comparable_to
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_convert_relation_class(
    dataset, class_from, class_to, dataset_after
):
    dataset.convert_relation_class(class_from, class_to)
    assert dataset.to_list() == dataset_after.to_list()


@pytest.mark.parametrize(
    "dataset, class_from, class_to, dataset_after",
    [
        ("empty", "none", "nothing", "empty"),              # none class doesn't exist
        ("small", "none", "pingu", "small"),                # none class doesn't exist
        ("large", "none", "planet", "large"),               # none class doesn't exist
        ("large", "SIMILAR_TO", "comparable_to", "large"),  # case sensitive
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_convert_missing_relation_class(
    dataset, class_from, class_to, dataset_after
):
    dataset.convert_relation_class(class_from, class_to)
    assert dataset.to_list() == dataset_after.to_list()


# Test flatten all entities
@pytest.mark.parametrize(
    "dataset, dataset_after",
    [
        ("empty", "empty"),
        ("small", "small"),  # small and medium should be unaffected
        ("medium", "medium"),
        ("large", "large_after_flatten_ec"),
        ("hierarchical", "hierarchical_after_flatten_ec"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_flatten_all_entities(dataset, dataset_after):
    dataset.flatten_all_entities()
    assert dataset.to_list() == dataset_after.to_list()


# Test flatten all relations
@pytest.mark.parametrize(
    "dataset, dataset_after",
    [
        ("empty", "empty"),
        ("small", "small"),  # small and medium should be unaffected
        ("medium", "medium"),
        ("large", "large_after_flatten_rc"),
        ("hierarchical", "hierarchical_after_flatten_rc"),
    ],
    indirect=["dataset", "dataset_after"],
)
def test_dataset_manip_flatten_all_relations(dataset, dataset_after):
    dataset.flatten_all_relations()
    assert dataset.to_list() == dataset_after.to_list()
