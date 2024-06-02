from langchain_community.document_loaders import MongodbLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pymongo
from langchain_community.embeddings import ollama
from langchain_community.vectorstores.chroma import Chroma
import os
import shutil

CHROMA_PATH = "chroma"


"""
It is very important to get the Ollama embedding function in this way.

The following import contains embedding function that works with Chroma db:
from langchain_community.embeddings import ollama

This does not:
from langchain_community.embeddings import OllamaEmbeddings
"""
def get_embedding_function():
    ollama_emb = ollama.OllamaEmbeddings(model='nomic-embed-text')

    return ollama_emb


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
        document_title = document_mongo["Title"]
        documents[i].metadata.update({"Title": document_title})

        document_link = document_mongo["Link"]

        if document_link is not None and document_link != "":
            documents[i].metadata.update({"Link": str(document_link)})
        else:
            documents[i].metadata.update({"Link": "Link not currently provided."})
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=8192,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


"""
On a local machine, run "ollama serve" to get the embeddings.

Embeddings are saved to the chroma database locally at "CHROMA_PATH".

We only add new chunks if either collection, title, or start index is different from existing chunks.
"""
def save_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks:
        chunk_chroma_id = chroma_id_format(chunk)
        if chunk_chroma_id not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks) > 0:
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids, duplicates = create_chroma_ids(new_chunks)
        for i in sorted(duplicates, reverse=True):
            del new_chunks[i]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add.")


"""
This is the way we will have unique IDs for each document in chromadb.

Chunks from the same document will have the same title, so start index is included as well.
"""
def chroma_id_format(chunk: Document) -> str:
    collection = chunk.metadata.get("collection")
    title = chunk.metadata.get("Title")
    start_index = chunk.metadata.get("start_index")
    return f"{collection}:{title}:{start_index}"


def create_chroma_ids(chunks: list[Document]):
    ids = set()
    duplicates = set()
    for i in range(len(chunks)):
        chunk_id = chroma_id_format(chunks[i])
        if chunk_id in ids:
            duplicates.add(i)
        ids.add(chunk_id)

    return list(ids), list(duplicates)


def pipeline():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["hpc_training_raw_local_db"]
    collections = db.list_collection_names()
    for collection in collections:
        documents = load_documents("hpc_training_raw_local_db", collection)
        chunks = chunk_documents(documents)
        save_to_chroma(chunks)


if __name__ == "__main__":
    pipeline()

