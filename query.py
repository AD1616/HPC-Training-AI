import argparse
from langchain_community.chat_models import ChatOllama
from generate_all_dense_embeddings import dense_relevant_ranked_documents
from sparse_embeddings import sparse_relevant_ranked_documents
from grade_documents import grade
from identify_training_materials import identify_documents
from rank_documents import rank_docs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    response, docs = generate_output(query_text)
    print(response)


def generate_output(query_text: str):
    dense_results = dense_relevant_ranked_documents(query_text, 20)
    sparse_results = sparse_relevant_ranked_documents(query_text, 20)

    if len(dense_results) == 0 and len(sparse_results) == 0:
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    relevant_dense_documents, irrelevant_dense_documents = grade(dense_results, query_text)
    relevant_sparse_documents, irrelevant_sparse_documents = grade(sparse_results, query_text)

    if len(relevant_dense_documents) == 0 and len(relevant_sparse_documents):
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    training_dense_documents, paper_dense_documents = identify_documents(relevant_dense_documents)
    training_sparse_documents, paper_sparse_documents = identify_documents(relevant_sparse_documents)

    if len(training_dense_documents) == 0 and len(training_sparse_documents) == 0:
        print("Unable to find matching results.")
        return "Unable to find matching results.", []

    all_documents = []
    for document in training_sparse_documents:
        found = False
        # found_display = False
        for existing in all_documents:
            if existing.metadata.get("id") == document.metadata.get("id"):
                found = True
            # if existing.metadata.get("Title") == document.metadata.get("Title"):
            #     found_display = True
        if not found:
            all_documents.append(document)
        # if not found_display:
        #     display_documents.append(document)

    for document in training_dense_documents:
        found = False
        for existing in all_documents:
            if existing.metadata.get("id") == document.metadata.get("id"):
                found = True
        if not found:
            all_documents.append(document)

    reranked_documents = rank_docs(all_documents, query_text)

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

    return response_text, all_documents


if __name__ == "__main__":
    main()