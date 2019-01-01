from flask import Flask, render_template, request
from crawler import Crawler

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    length = ""
    if request.form:
        url = Crawler(request.form.get("url"))
        length = url.run()

    return render_template("home.html", length=length)

