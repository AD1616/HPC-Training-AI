from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import pymongo
from langchain_community.vectorstores.chroma import Chroma
from preprocess_documents import load_documents
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"


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


def dense_relevant_ranked_documents(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search(query_text, k=5)

    return results


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
