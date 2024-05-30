import argparse
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import ollama
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}

The format of the answer should be a numbered list of relevant materials or events.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = ollama.OllamaEmbeddings(model='nomic-embed-text')
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search(query_text, k=3)
    if len(results) == 0:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOllama(model="llama3")
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("Title", None) for doc in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()