from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eng")
def eng_index():
    return render_template("englishMain.html")

#tilaaSossuKeikalle
@app.route("/tilaasossu")
def tilaa():
	return render_template("tilaasossu.html")

@app.route("/order")
def order():
    return render_template("order.html")

#mitenSoittajaksi
@app.route("/mukaan")
def mukaan():
	return render_template("tulemukaan.html")

@app.route("/joinsossu")
def join():
    return render_template("joinsossu.html")

#ajankohtaista
@app.route("/ajankohtaista")
def ajankohtaista():
    try:
        file = open("instagram_media.json", "r")
        media = json.loads(file.read())
    except FileNotFoundError:
        return render_template("index.html")
    return render_template('ajankohtaista.html', media=media)
