from flask import Flask, render_template
import json

app = Flask(__name__)

class NavbarItem():
    def __init__(self, url, template, title, picture):
        self.url = url
        self.title = title
        self.template = template
        self.picture = picture

# Navbar definitions in different languages
navbars = {
    "fi": [
        NavbarItem("etusivu",       "index.html",         "Etusivu",            "tulemukaan.jpg"),
        NavbarItem("tilaa",         "tilaa_sossu.html",   "Tilaa meidät", "tilaameidat.jpg"),
        NavbarItem("mukaan",        "tule_mukaan.html",   "Tule mukaan", "tulemukaan.jpg"),
        NavbarItem("ajankohtaista", "ajankohtaista.html", "Ajankohtaista", "ajankohtaista.jpg"),
        NavbarItem("sitsilaulu22", "sitsilaulu22.html", "Sitsilaulukonsertti", "sitsilaulut.jpg"),
    ],
    "en": [
        NavbarItem("main",          "english_main.html",  "Main", "tulemukaan.jpg"),
        NavbarItem("bookus",        "book_sossu.html",    "Book us", "tilaameidat.jpg"),
        NavbarItem("join",          "join_sossu.html",    "Join SOSSu", "tulemukaan.jpg"),
        NavbarItem("socialmedia",   "ajankohtaista.html", "Social Media", "ajankohtaista.jpg"),
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
                print(item.picture)
                return render_template(item.template,
                        navbar=getNavbarDict(lang),
                        active=index,
                        lang=lang,
                        pictureId=item.picture)
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
            navbar=getNavbarDict(lang),
            pictureId="ajankohtaista.jpg")
