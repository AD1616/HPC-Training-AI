import pymongo
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
from aggregate_documents import load_mongo_documents, CHROMA_PATH, MONGODB_NAME, MONGODB_URL


def chunk_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
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
    print(f"Mongo: Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks:
        chunk_chroma_id = chroma_id_format(chunk)
        if chunk_chroma_id not in existing_ids:
            new_chunks.append(chunk)
            chunk.metadata.update({"id": chunk_chroma_id})

    if len(new_chunks) > 0:
        print(f"Mongo: Adding new documents: {len(new_chunks)}")
        new_chunk_ids, duplicates = create_chroma_ids(new_chunks)
        for i in sorted(duplicates, reverse=True):
            del new_chunks[i]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("Mongo: No new documents to add.")


"""
This is the way we will have unique IDs for each document FOR MONGODB DATA in chromadb.

Chunks from the same document will have the same title, so start index is included as well.

Note that pdf data and mongodb data will have a separate template for ids.
The below data should only be used to check for existence of data that came from mongodb.
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


def mongo_pipeline():
    client = pymongo.MongoClient(MONGODB_URL)
    db = client[MONGODB_NAME]
    collections = db.list_collection_names()
    for collection in collections:
        documents = load_mongo_documents(MONGODB_NAME, collection)
        chunks = chunk_documents(documents)
        save_to_chroma(chunks)


if __name__ == "__main__":
    mongo_pipeline()