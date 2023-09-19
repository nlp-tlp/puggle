from ettools import Dataset

d = Dataset("test.json")

# for doc in d.documents:
#    print("--")
#    print(doc.to_dict())

d.load_into_neo4j(recreate=True)
