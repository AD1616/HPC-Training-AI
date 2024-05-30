from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import ollama

CHROMA_PATH = "../chroma"


def get_embedding_function():
    ollama_emb = ollama.OllamaEmbeddings(model='nomic-embed-text')

    return ollama_emb


def main():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    query = "Cyberinfrastructure"
    docs = db.similarity_search(query)

    print(docs[0].metadata.get("Title"))


if __name__ == "__main__":
    main()