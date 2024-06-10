import argparse
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from generate_all_dense_embeddings import dense_relevant_ranked_documents
from sparse_embeddings import sparse_relevant_ranked_documents
from langchain.schema import Document


PROMPT_TEMPLATE = """
Answer the question based only on the following sources:

{context}

---

Answer the question by providing ONLY a bulleted list of sources (NO OTHER WORDS)
with titles and URLs ONLY coming from the above list: {question}
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
    dense_results = dense_relevant_ranked_documents(query_text, 10)
    sparse_results = sparse_relevant_ranked_documents(query_text, 10)

    if len(dense_results) == 0 or len(sparse_results) == 0:
        print("Unable to find matching results.")
        return

    for doc in dense_results:
        print("Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link"))
    print("-----------------")
    for doc in sparse_results:
        print("Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link"))
    print("-----------------")

    dense_prompt = generate_dense_context(dense_results, query_text)
    sparse_prompt = generate_sparse_context(sparse_results, query_text)

    model = ChatOllama(model=model)
    dense_response_text = model.predict(dense_prompt)
    sparse_response_text = model.predict(sparse_prompt)

    context_text = dense_response_text + sparse_response_text + "DELETE ALL TEXT BEFORE THE BULLETS"
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    response_text = model.predict(prompt)

    print(response_text)
    return response_text


def generate_dense_context(docs: list[Document], query_text: str):
    context_text = ""
    context_text += "\n\nHere are 10 relevant sources from general context: \n\n"
    context_text += "\n\n---\n\n".join(["Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link")
                                        + "Content: " + doc.page_content for doc in docs])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    return prompt


def generate_sparse_context(docs: list[Document], query_text: str):
    context_text = ""
    context_text += "\n\nHere are 10 relevant sources from keywords: \n\n"
    context_text += "\n\n---\n\n".join(["Title: " + doc.metadata.get("Title") + " URL: " + doc.metadata.get("Link")
                                        for doc in docs])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    return prompt


if __name__ == "__main__":
    main()