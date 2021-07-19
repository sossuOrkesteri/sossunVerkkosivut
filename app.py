from flask import Flask
app = Flask(__name__)
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

#tilaaSossuKeikalle
@app.route("/tilaasossu")
def tilaa():
	return render_template("tilaasossu.html")

#mitenSoittajaksi
@app.route("/mukaan")
def mukaan():
	return render_template("tulemukaan.html")

#ajankohtaista
@app.route("/ajankohtaista")
def ajankohtaista():
	return "Somet"
