from langchain_community.document_loaders import MongodbLoader, PyPDFDirectoryLoader
from langchain.schema import Document
import pymongo
from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function

DATA_PATH = "pdf_data"

CHROMA_PATH = "chroma"

MONGODB_URL = "mongodb://localhost:27017/"

MONGODB_NAME = "hpc_training_raw_local_db"

LLM_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


"""
Creates langchain documents from MongoDB entries.

Note that metadata, particularly "Title" of each document, is additionally part of document content.
The intention for this is to account for titles including keywords that may not otherwise be present.
"""

def load_mongo_documents(db_name: str, collection_name: str) -> list[Document]:
    loader = MongodbLoader(
        connection_string=MONGODB_URL,
        db_name=db_name,
        collection_name=collection_name,
    )

    documents = loader.load()
    client = pymongo.MongoClient(MONGODB_URL)
    db = client[db_name]
    collection = db[collection_name]
    for i in range(len(documents)):
        document_mongo = collection.find_one({"_id": i})
        document_title = document_mongo.get("Title")
        documents[i].metadata.update({"Title": document_title})

        document_link = str(document_mongo.get("Link"))

        if document_link is not None:
            document_link = document_link.strip()

        if document_link is not None and document_link != "" and document_link[0] != '[':
            documents[i].metadata.update({"Link": str(document_link)})
        else:
            documents[i].metadata.update({"Link": "Link not currently provided."})
    return documents


def load_pdf_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = document_loader.load()
    for document in documents:
        document.metadata["Title"] = document.metadata["source"][9:-4]
        document.metadata["Link"] = "Link not provided."
    return documents


def get_all_documents():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    data = db.get(include=['metadatas', 'documents'])
    total = total_documents()

    docs = []
    for i in range(total):
        content = data['documents'][i]
        metadata = data['metadatas'][i]
        doc = Document(page_content=content, metadata=metadata)
        docs.append(doc)

    return docs


def total_documents():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    return len(db.get(include=[])['ids'])


if __name__ == "__main__":
    print(total_documents())
    print(get_all_documents()[2000])