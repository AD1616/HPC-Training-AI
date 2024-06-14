from flask import Flask, render_template, request, session
from query import generate_output

DEVELOPMENT_ENV = True

app = Flask(__name__)
app.secret_key = 'HPC-AI'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/test")
def test():
    return render_template("test.html")


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
    

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, host='localhost')