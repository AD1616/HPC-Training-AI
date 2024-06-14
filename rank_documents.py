from sentence_transformers import CrossEncoder
from langchain.schema import Document

"""
Reranking documents with a cross encoder based on relevance to query.
"""
def rank_docs(documents: list[Document], query: str):
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    ranks = model.rank(query, [document.page_content for document in documents])

    reordered = []
    for rank in ranks:
        reordered.append(documents[rank['corpus_id']])

    return reordered


if __name__ == "__main__":
    pass
