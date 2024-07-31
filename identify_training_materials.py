from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
from aggregate_documents import CHROMA_PATH, total_documents, LLM_MODEL
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document


"""
Takes in a list of documents

Outputs which of those documents are research papers and which are training materials.
"""
def identify_documents(documents: list[Document]):
    # llm = ChatOllama(model=LLM_MODEL, format="json", temperature=0)
    inference_server_url = "https://sdsc-llm-api.nrp-nautilus.io/"

    llm = ChatOpenAI(
        model=LLM_MODEL,
        openai_api_key="js8CT4Cs6HShr8Ct2X",
        openai_api_base=inference_server_url,
        temperature=0,
    )

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether
        a document is a research paper. Carefully look at the title to identify if it is a research paper, looking for 
        things like authors and dates. Try not to incorrectly label any material as a research paper if it is not. \n
        Your identification can be "paper" or "training". \n
        Provide the identification as a JSON with a single key 'identification' and no preamble or explanation.
         <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here is the retrieved document: \n\n {document} \n
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["document"],
    )

    retrieval_grader = prompt | llm | JsonOutputParser()

    training_documents = []
    paper_documents = []
    for document in documents:
        identification = retrieval_grader.invoke(
            {"document": document.metadata.get("Title")})["identification"]
        if identification == "training":
            training_documents.append(document)
        if identification == "paper":
            paper_documents.append(document)

    return training_documents, paper_documents


def identify_query(question: str):
    llm = ChatOllama(model=LLM_MODEL, format="json", temperature=0)

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether a user 
        is looking for only training materials in response to a query or not. If the question specifically mentions 
        learning about a topic or asks for resources about a topic, then label it as "training". 
        The goal is to filter documents to only training materials if that is what the user indicates. \n
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

    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

    question = "parallel computing"

    documents = retriever.invoke(question)

    training_documents, paper_documents = identify_documents(documents)

    for document in training_documents:
        print(document.metadata.get("Title"))