from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
from aggregate_documents import CHROMA_PATH, total_documents, LLM_MODEL
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document


"""
Takes in a list of documents and a string question.

Outputs which of those documents are relevant to the question and which are not, both as lists.
"""
def guided_response(documents: list[Document], question: str):
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    # inference_server_url = "https://sdsc-llama3-api.nrp-nautilus.io/v1"
    #
    # llm = ChatOpenAI(
    #     model=LLM_MODEL,
    #     openai_api_key="js8CT4Cs6HShr8Ct2X",
    #     openai_api_base=inference_server_url,
    #     temperature=0
    # )

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert on High Performance
        computing. You will be given a user query along with a list of potentially helpful documents in answering that query.
        Answer the query, and provide helpful guidance for further learning. Do not provide a preamble. \n
         <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here are the retrieved documents: \n\n {documents} \n\n
        Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "documents"],
    )

    generator = prompt | llm

    document_text = ""
    for document in documents:
        doc_content = document.page_content
        doc_title = document.metadata.get("Title")
        doc_link = document.metadata.get("Link")
        document_text += f"\n Title: {doc_title} Link: {doc_link} \n Content: {doc_content} \n"

    output = generator.invoke({"question": question, "documents": document_text})

    return output.content


if __name__ == "__main__":
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    question = "parallel computing"

    documents = retriever.invoke(question)

    output = guided_response(documents, question)

    print(output)