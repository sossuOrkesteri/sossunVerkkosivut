from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Moi!"

#tilaaSossuKeikalle
@app.route("/tilaasossu")
def tilaa():
	return "Moimoi!"

#mitenSoittajaksi
@app.route("/mukaan")
def mukaan():
	return "Tervetuloa"

#ajankohtaista
@app.route("/ajankohtaista")
def ajankohtaista():
	return "Somet"


