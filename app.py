"""Simple Flask app to test the CI/CD pipeline."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def hello_world():
    """Return a simple message."""

    return render_template("home.html")


@app.route("/market")
def market():
    """Return a simple message."""

    return render_template("market.html", item_name="Phone", item_price=500)


@app.route("/crossword")
def crossword():
    """Return a simple message."""

    return render_template("crossword.html", rows=15, cols=15)
