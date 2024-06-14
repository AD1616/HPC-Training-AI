import argparse
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from generate_all_dense_embeddings import dense_relevant_ranked_documents
from sparse_embeddings import sparse_relevant_ranked_documents
from grade_documents import grade
from identify_training_materials import identify_documents

PROMPT_TEMPLATE = """
Find documents relevant to the user question only from the following list:

{context}

---

Provide a numbered list of sources with titles and URLs ONLY coming from the above list, relating to the following question: {question}
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


def generate_output(context_text: str, query_text: str, model: str):

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOllama(model=model)
    response_text = model.predict(prompt)

    return response_text


if __name__ == "__main__":
    main()