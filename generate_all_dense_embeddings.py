import generate_dense_pdf_embeddings
import generate_dense_mongo_embeddings
from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
from aggregate_documents import CHROMA_PATH, total_documents


def pipeline():
    # handle mongodb data
    generate_dense_mongo_embeddings.mongo_pipeline()

    # handle pdf data
    generate_dense_pdf_embeddings.pdf_pipeline()


def dense_relevant_ranked_documents(query_text: str, num_docs: int):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search(query_text, k=num_docs)

    return results


if __name__ == "__main__":
    pipeline()