from langchain_community.embeddings import ollama
# from langchain_community.embeddings import HuggingFaceEmbeddings


"""
It is very important to get the Ollama embedding function in this way.

The following import contains embedding function that works with Chroma db:
from langchain_community.embeddings import ollama

This does not:
from langchain_community.embeddings import OllamaEmbeddings
"""
# def get_embedding_function():
#     ollama_emb = ollama.OllamaEmbeddings(
#         base_url='https://llm-sdsc-ollama.nrp-nautilus.io',
#         model='nomic-embed-text'
#     )
#
#     return ollama_emb


def get_embedding_function():
    ollama_emb = ollama.OllamaEmbeddings(model='nomic-embed-text')

    return ollama_emb


def get_hg_embedding_function():
    # vectorizer = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #
    # return vectorizer
    pass