import argparse
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from generate_dense_embeddings import dense_relevant_ranked_documents
from sparse_embeddings import sparse_relevant_ranked_documents

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following sources:

{context}

---

Answer the question by providing a numbered list of sources with titles, URLs, and descriptions ONLY coming from the above list: {question}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument("model", type=str, help="model")
    args = parser.parse_args()
    query_text = args.query_text
    model = args.model

    formatted_response = generate_output(query_text, model)
    print(formatted_response)


def generate_output(query_text: str, model: str):
    dense_results = dense_relevant_ranked_documents(query_text)
    sparse_results = sparse_relevant_ranked_documents(query_text)

    # for doc in dense_results:
    #     print("Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link"))
    # print("-----------------")
    # for doc in sparse_results:
    #     print("Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link"))
    # print("-----------------")

    if len(dense_results) == 0 or len(sparse_results) == 0:
        print("Unable to find matching results.")
        return

    context_text = ""
    context_text += "\n\nHere are 5 relevant sources based on keywords: \n\n"
    context_text += "\n\n---\n\n".join(["Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link") for doc in sparse_results])
    context_text += "\n\nHere are 5 relevant sources based on general context: \n\n"
    context_text += "\n\n---\n\n".join(["Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link") for doc in dense_results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOllama(model=model)
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("Title", None) for doc in dense_results]
    # formatted_response = f"Response: {response_text}\n Sources:{sources}"
    formatted_response = f"Response: {response_text}"
    return formatted_response


if __name__ == "__main__":
    main()