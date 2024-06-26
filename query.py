import argparse
from langchain_community.chat_models import ChatOllama
from generate_all_dense_embeddings import dense_relevant_ranked_documents
from sparse_embeddings import sparse_relevant_ranked_documents
from grade_documents import grade
from identify_training_materials import identify_documents
from rank_documents import rank_docs
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    response, docs = generate_output(query_text)
    print(response)


def generate_output(query_text: str):
    start = time.time()
    dense_results = dense_relevant_ranked_documents(query_text, 20)
    end = time.time()
    time_dense = end - start

    start = time.time()
    sparse_results = sparse_relevant_ranked_documents(query_text, 20)
    end = time.time()
    time_sparse = end - start

    if len(dense_results) == 0 and len(sparse_results) == 0:
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    start = time.time()
    relevant_dense_documents, irrelevant_dense_documents = grade(dense_results, query_text)
    end = time.time()
    time_relevant_dense = end - start

    start = time.time()
    relevant_sparse_documents, irrelevant_sparse_documents = grade(sparse_results, query_text)
    end = time.time()
    time_relevant_sparse = end - start

    if len(relevant_dense_documents) == 0 and len(relevant_sparse_documents):
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    start = time.time()
    training_dense_documents, paper_dense_documents = identify_documents(relevant_dense_documents)
    end = time.time()
    time_training_dense = end - start

    start = time.time()
    training_sparse_documents, paper_sparse_documents = identify_documents(relevant_sparse_documents)
    end = time.time()
    time_training_sparse = end - start

    if len(training_dense_documents) == 0 and len(training_sparse_documents) == 0:
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    start = time.time()
    all_documents = []
    for document in training_sparse_documents:
        found = False
        for existing in all_documents:
            if existing.metadata.get("id") == document.metadata.get("id"):
                found = True
        if not found:
            all_documents.append(document)

    for document in training_dense_documents:
        found = False
        for existing in all_documents:
            if existing.metadata.get("id") == document.metadata.get("id"):
                found = True
        if not found:
            all_documents.append(document)
    end = time.time()
    time_unique = end - start

    start = time.time()
    reranked_documents = rank_docs(all_documents, query_text)
    end = time.time()
    time_rerank = end - start

    start = time.time()
    display_docs = []
    for document in reranked_documents:
        found = False
        for existing in display_docs:
            if existing.metadata.get("Title") == document.metadata.get("Title"):
                found = True
        if not found:
            display_docs.append(document)

    response_text = ""
    for document in display_docs:
        response_text += f"\n\n{document.metadata.get('Title')} \n {document.metadata.get('Link')} \n"

    end = time.time()
    time_display = end - start

    print(f"Dense retrieval: {time_dense}")
    print(f"Sparse retrieval: {time_sparse}")
    print(f"Relevant dense: {time_relevant_dense}")
    print(f"Relevant sparse: {time_relevant_sparse}")
    print(time_training_dense)
    print(time_training_sparse)
    print(time_unique)
    print(time_rerank)
    print(time_display)
    return response_text, all_documents


if __name__ == "__main__":
    main()