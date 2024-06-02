from flask import Flask, render_template, request
from query import generate_output

DEVELOPMENT_ENV = True

app = Flask(__name__)


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
    return generate_output(query, "llama3")


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)