import argparse
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following sources:

{context}

---

Answer the question by providing a numbered list of sources with titles, URLs and descriptions ONLY coming from the above list: {question}
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
    embedding_function = ollama.OllamaEmbeddings(model='nomic-embed-text')
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search(query_text, k=20)
    if len(results) == 0:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content + str(doc.metadata) for doc in results])
    print(context_text)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOllama(model=model)
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("Title", None) for doc in results]
    # formatted_response = f"Response: {response_text}\n Sources:{sources}"
    formatted_response = f"Response: {response_text}"
    return formatted_response


if __name__ == "__main__":
    main()