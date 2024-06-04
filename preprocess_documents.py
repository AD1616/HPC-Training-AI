from langchain_community.document_loaders import MongodbLoader
from langchain.schema import Document
import pymongo

"""
Creates langchain documents from MongoDB entries.

Note that metadata, particularly "Title" of each document, is additionally part of document content.
The intention for this is to account for titles including keywords that may not otherwise be present.
"""


def load_documents(db_name: str, collection_name: str) -> list[Document]:
    loader = MongodbLoader(
        connection_string="mongodb://localhost:27017/",
        db_name=db_name,
        collection_name=collection_name,
    )

    documents = loader.load()
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]
    for i in range(len(documents)):
        document_mongo = collection.find_one({"_id": i})
        document_title = document_mongo.get("Title")
        documents[i].metadata.update({"Title": document_title})

        document_link = str(document_mongo.get("Link"))

        if (document_link is not None):
            document_link = document_link.strip()

        if document_link is not None and document_link != "" and document_link[0] != '[':
            documents[i].metadata.update({"Link": str(document_link)})
        else:
            documents[i].metadata.update({"Link": "Link not currently provided."})
    return documents


def get_all_documents():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["hpc_training_raw_local_db"]
    collections = db.list_collection_names()

    data = []
    for collection in collections:
        data += load_documents("hpc_training_raw_local_db", collection)

    return data


if __name__ == "__main__":
    data = get_all_documents()
    print(data)
