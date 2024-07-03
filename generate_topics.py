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
def topics(documents: list[Document], question: str):
    inference_server_url = "https://sdsc-llama3-api.nrp-nautilus.io/v1"

    llm = ChatOpenAI(
        model=LLM_MODEL,
        openai_api_key="js8CT4Cs6HShr8Ct2X",
        openai_api_base=inference_server_url,
        temperature=0,
    )

    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert in High Performance 
        Computing. You will be given a user question, and you need to identify the topics related to this question. 
        You should then provide relevant topics to the user question. These topics should help the user learn about the 
        original topic, and should be related to High Performance Computing. For each topic, also come up with a 
        thorough prompt that describes it and asks for materials related to it. \n
        Put each topic with its prompt, separated by the "_" character. Do not include any new lines. This is called a 
        pair. Put all of the pairs together, separated by the "|" character. Again, do not include any new lines. 
        Omit any preamble. Put everything on the same line. \n
         <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "document"],
    )

    generator = prompt | llm

    document_text = ""
    for document in documents:
        doc_content = document.page_content
        doc_title = document.metadata.get("Title")
        doc_link = document.metadata.get("Link")
        document_text += f"\n Title: {doc_title} Link: {doc_link} \n Content: {doc_content} \n"

    output = generator.invoke({"question": question, "document": document_text}).content

    pairs = output.split('|')
    topic_list = []
    for i in range(1, len(pairs)):
        components = pairs[i].split('_')
        topic_list.append((components[0], components[1]))

    return topic_list


if __name__ == "__main__":
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    question = "parallel computing"

    documents = retriever.invoke(question)

    topic_list = topics(documents=documents, question=question)

    for topic in topic_list:
        print(topic)