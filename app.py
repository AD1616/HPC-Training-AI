from flask import Flask, render_template, request, session
from query import generate_output
from answer import guided_response
from langchain_community.vectorstores.chroma import Chroma
from langchain.schema import Document
from aggregate_documents import CHROMA_PATH
from get_embedding_function import get_embedding_function
from roadmaps.map_endpoints import map_bp

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.secret_key = 'HPC-AI'

app.register_blueprint(map_bp, url_prefix='/roadmaps')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/test")
def test():
    return render_template("test.html")


"""
Endpoint to return list of relevant documents to query.
"""
@app.route("/output")
def output():
    query = request.args.get('query')
    try:
        session['documents'] = []
        response, documents = generate_output(query)
        for document in documents:
            session['documents'].append(document.metadata)
        return response
    except:
        return "AI service is not running."


"""
Endpoint to generate description to elaborate on query based on relevant documents.
"""
@app.route("/guide")
def guide():
    query = request.args.get('query')
    document_data = session['documents']
    documents = []
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    for document in document_data:
        doc_obj = db.get(include=['metadatas', 'documents'], where={"id": document.get('id')})
        content = doc_obj['documents'][0]
        metadata = doc_obj['metadatas'][0]
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
    response = guided_response(documents, query)
    return response


@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")


@app.route("/dynamic")
def dynamic():
    return render_template("dynamic_generation.html")
    

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, host='localhost')