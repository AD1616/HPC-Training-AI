from langchain_community.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
from aggregate_documents import CHROMA_PATH, LLM_MODEL
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import Document


"""
Takes in a list of documents and a string question.

Outputs a list that consists of pairs, where each pair has a topic and a corresponding prompt.
"""
def topics(documents: list[Document], question: str):
    inference_server_url = "https://sdsc-llm-api.nrp-nautilus.io/"

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
        original topic, and should be related to High Performance Computing. The topics should cover different content, 
        and should not depend on each other. Try to keep the name of the topic to one or two words. For each topic, 
        also come up with a thorough prompt that describes it and asks for materials related to it. \n
        Give your response in JSON, with each topic being the key and its corresponding prompt being the value. 
        Omit any preamble. 
         <|eot_id|><|start_header_id|>user<|end_header_id|>
        Here is the retrieved document: \n\n {document} \n\n
        Here is the user question: {question} \n <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question", "document"],
    )

    generator = prompt | llm | JsonOutputParser()

    document_text = ""
    for document in documents:
        doc_content = document.page_content
        doc_title = document.metadata.get("Title")
        doc_link = document.metadata.get("Link")
        document_text += f"\n Title: {doc_title} Link: {doc_link} \n Content: {doc_content} \n"

    output = generator.invoke({"question": question, "document": document_text})

    topic_list = []
    for topic in output:
        topic_list.append((topic, output[topic]))

    return topic_list


if __name__ == "__main__":
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    question = "parallel computing"

    documents = retriever.invoke(question)

    topic_list = topics(documents=documents, question=question)

    for topic in topic_list:
        print(topic)
