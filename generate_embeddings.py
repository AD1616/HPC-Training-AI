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
        document_title = collection.find_one({"_id": i})["Title"]
        documents[i].metadata.update({"Title": document_title})
    return documents


def chunk_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


"""
On a local machine, run "ollama serve" to get the embeddings.

Embeddings are saved to the chroma database locally at "CHROMA_PATH".
"""
def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # automatically saves to directory "CHROMA_PATH"
    db = Chroma.from_documents(
        chunks, get_embedding_function(), persist_directory=CHROMA_PATH
    )

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def pipeline():
    documents = load_documents("hpc_training_raw_local_db", "sdsc_events")
    chunks = chunk_documents(documents)
    save_to_chroma(chunks)


if __name__ == "__main__":
    pipeline()

