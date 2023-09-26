from puggle import Dataset

d = Dataset()
# d.load_documents("sample_data/documents.csv")
d.load_documents("sample_data/documents.csv", "sample_data/annotations.json")

for doc in d.documents:
    print("--")
    print(doc.to_dict())

d.load_into_neo4j(recreate=True)
