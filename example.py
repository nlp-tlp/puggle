from puggle import Dataset, Document, Annotation

d = Dataset()
# d.load_documents("sample_data/documents.csv", "sample_data/annotations.json")

f1 = {"text": "one three two", "date": "12/05/2020", "x": "4", "y": "test"}
a1 = Annotation.from_dict(
    {
        "tokens": ["one", "three", "two"],
        "mentions": [
            {"start": 0, "end": 1, "labels": ["number"]},
            {"start": 1, "end": 2, "labels": ["number"]},
            {"start": 2, "end": 3, "labels": ["number"]},
        ],
        "relations": [
            {"start": 1, "end": 0, "type": "bigger_than"},
            {"start": 1, "end": 2, "type": "bigger_than"},
        ],
    },
)

doc1 = Document(f1, a1)
d.add_document(doc1)

f2 = {"text": "four six five", "date": "04/05/2020", "x": "12", "y": "another"}
a2 = Annotation.from_dict(
    {
        "tokens": ["four", "six", "five"],
        "mentions": [
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


for doc in d.documents:
    print("--")
    print(doc.to_dict())

d.load_into_neo4j(recreate=True)
