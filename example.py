from puggle import Dataset, Document, Annotation

d = Dataset()
d.load_documents(
    sd_filename="sample_data/documents.csv",
    anns_filename="sample_data/annotations.json",
    anns_format="spert",
)

for doc in d.documents:
    print("--")
    print(doc.to_dict())

d.load_into_neo4j(recreate=True)
