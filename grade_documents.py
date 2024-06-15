from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
from aggregate_documents import CHROMA_PATH, total_documents, LLM_MODEL
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document


"""
Takes in a list of documents and a string question.

Outputs which of those documents are relevant to the question and which are not, both as lists.
"""
def grade(documents: list[Document], question: str):
    # llm = ChatOllama(model=LLM_MODEL, format="json", temperature=0)
    inference_server_url = "https://sdsc-llama3-api.nrp-nautilus.io/v1"

    llm = ChatOpenAI(
        model=LLM_MODEL,
        openai_api_key="js8CT4Cs6HShr8Ct2X",
        openai_api_base=inference_server_url,
        temperature=0,
    )

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing relevance 
        of a retrieved document to a user question. If the document contains keywords related to the user question, 
        grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
         <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "document"],
    )

    retrieval_grader = prompt | llm | JsonOutputParser()

    relevant_documents = []
    irrelevant_documents = []
    for document in documents:
        doc_txt = document.page_content
        score = retrieval_grader.invoke({"question": question, "document": doc_txt})["score"]
        if score == "yes":
            relevant_documents.append(document)
        if score == "no":
            irrelevant_documents.append(document)

    return relevant_documents, irrelevant_documents


if __name__ == "__main__":
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    question = "parallel computing"

    documents = retriever.invoke(question)

    relevant_documents, irrelevant_documents = grade(documents, question)

    for document in relevant_documents:
        print(document.metadata.get("Title"))