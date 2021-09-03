from flask import Flask, render_template
import json

app = Flask(__name__)

class NavbarItem():
    def __init__(self, url, template, title):
        self.url = url
        self.title = title
        self.template = template

# Navbar definitions in different languages
navbars = {
    "fi": [
        NavbarItem("etusivu",       "index.html",         "Etusivu"),
        NavbarItem("tilaa",         "tilaa_sossu.html",   "Tilaa meidät keikalle"),
        NavbarItem("mukaan",        "tule_mukaan.html",   "Tule mukaan"),
        NavbarItem("ajankohtaista", "ajankohtaista.html", "Ajankohtaista"),
    ],
    "en": [
        NavbarItem("main",          "english_main.html",  "Main"),
        NavbarItem("bookus",        "book_sossu.html",    "Book us"),
        NavbarItem("join",          "join_sossu.html",    "Join SOSSu"),
        NavbarItem("socialmedia",   "ajankohtaista.html", "Social Media"),
    ]
}

def getNavbarDict(lang):
    return {item.url:item.title for item in navbars[lang]}

# Default routes, defined by navbar items
@app.route("/<page>")
@app.route("/", defaults={"page": navbars["fi"][0].url})
def getPage(page):
    for lang in ["en", "fi"]:
        for index,item in enumerate(navbars[lang]):
            if page == item.url:
                return render_template(item.template,
                        navbar=getNavbarDict(lang),
                        active=index,
                        lang=lang)
    return render_template("error.html", navbar=getNavbarDict("en"), msg="Page not found")

# social media tab is defined explicitly because of the extra data it needs
@app.route("/ajankohtaista", defaults={"lang": "fi"})
@app.route("/socialmedia", defaults={"lang": "en"})
def some(lang):
    try:
        file = open("instagram_media.json", "r")
        media = json.loads(file.read())
    except FileNotFoundError as err:
        return render_template("error.html", msg=str(err))
    return render_template('ajankohtaista.html',
            media=media,
            lang=lang,
            navbar=getNavbarDict(lang))
