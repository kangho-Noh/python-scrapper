from flask import Flask

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return "Hello! Welcome to mi casa!"


@app.route("/contact")
def contact():
    return "Contact me!"


app.run(host="127.0.0.1")
