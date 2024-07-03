from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from langchain.schema import Document
from aggregate_documents import get_all_documents
import pickle


"""
Tfidf Vectorizer takes in string data for page content of every document

return embeddings, the vectorizer fit to the data, and the length of the used data
"""
def generate_sparse_embeddings(documents: list[Document]):
    content = []
    for document in documents:
        content.append(document.page_content)
    vectorizer = TfidfVectorizer()
    data_embeddings = vectorizer.fit_transform(content)
    return data_embeddings, vectorizer, len(content)


"""
Related data to sparse embeddings is stored in a pickle file

pickle file has length 3 tuple:
(data_embeddings, vectorizer, length)

length is used to determine if there is any new data; if there is, regenerate Tfidf vectorizer

This will be useful once there is a lot of data and generating embeddings takes a while
"""
def load_sparse_embeddings():
    try:
        embeddings_and_vectorizer = pickle.load(open("sparse_embeddings.pickle", "rb"))
        data = get_all_documents()
        if len(data) > embeddings_and_vectorizer[2]:
            return dump_sparse_embeddings()
        else:
            return embeddings_and_vectorizer[0], embeddings_and_vectorizer[1], embeddings_and_vectorizer[2]
    except(OSError, IOError) as e:
        return dump_sparse_embeddings()


def dump_sparse_embeddings():
    data_embeddings, vectorizer, length = generate_sparse_embeddings(get_all_documents())
    pickle.dump((data_embeddings, vectorizer, length), open("sparse_embeddings.pickle", "wb"))
    return data_embeddings, vectorizer, length


def sparse_relevant_ranked_documents(query: str, num_docs: int):
    data = get_all_documents()
    data_embeddings, vectorizer, length = load_sparse_embeddings()

    query_embedding = vectorizer.transform([query])

    similarities = cosine_similarity(data_embeddings, query_embedding)
    ranked_indices = np.argsort(similarities, axis=0)[::-1].flatten()
    ranked_documents = [data[i] for i in ranked_indices]

    final = []
    for i in range(len(ranked_documents)):
        if len(final) == num_docs:
            break
        found = False
        for j in range(len(final)):
            if final[j].metadata["id"] == ranked_documents[i].metadata["id"]:
                found = True
                break
        if not found:
            final.append(ranked_documents[i])

    # return ranked_documents[:num_docs]
    return final


def main():
    documents = sparse_relevant_ranked_documents("ciml", 15)

    for doc in documents:
        print(doc.metadata.get("Title"))


if __name__ == "__main__":
    main()