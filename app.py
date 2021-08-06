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
    return render_template("tilaasossu.html", luokka1="active",luokka2="", luokka3="")

@app.route("/bookus")
def order():
    return render_template("order.html", luokka1="active",luokka2="", luokka3="")

#mitenSoittajaksi
@app.route("/mukaan")
def mukaan():
	return render_template("tulemukaan.html", luokka1="",luokka2="active", luokka3="")

@app.route("/joinsossu")
def join():
    return render_template("joinsossu.html", luokka1="",luokka2="active", luokka3="")

#ajankohtaista
@app.route("/ajankohtaista")
def ajankohtaista():
    try:
        file = open("instagram_media.json", "r")
        media = json.loads(file.read())
    except FileNotFoundError:
        return render_template("index.html")
    return render_template('ajankohtaista.html', media=media)
