from flask import Flask, render_template, request
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
        NavbarItem("tilaa",         "tilaa_sossu.html",   "Tilaa meidät"),
        NavbarItem("mukaan",        "tule_mukaan.html",   "Tule mukaan"),
        #NavbarItem("ajankohtaista", "ajankohtaista.html", "Ajankohtaista"),
        NavbarItem("sitsilaulu22",  "sitsilaulu22.html",  "Sitsilaulukonsertti"),
    ],
    "en": [
        NavbarItem("main",          "english_main.html",  "Main"),
        NavbarItem("bookus",        "book_sossu.html",    "Book us"),
        NavbarItem("join",          "join_sossu.html",    "Join SOSSu"),
        #NavbarItem("socialmedia",   "ajankohtaista.html", "Social Media"),
    ]
}

def validateUrl(url):
    """ Checks if the url is valid.
    Returns the language code of the navbar that the url was found from
    and the index of the url in that navbar.
    Returned index is None if the url is not found in any of the navbars."""
    for lang in ["en", "fi"]:
        for index,item in enumerate(navbars[lang]):
            if item.url == url:
                return lang, index
    return "en", None

def getErrorPage(msg):
    return render_template("error.html",
            navbar=navbars["en"],
            lang="en",
            msg=msg)

# Default routes, defined by navbar items
@app.route("/<url>")
# No url defaults to the first tab of the finnish navbar
@app.route("/", defaults={"url": navbars["fi"][0].url})
def getPage(url, **kwargs):
    """ Returns the fully rendered html page associated with the given url.
    Keyword arguments are passed to the to the templating engine. """
    lang, index = validateUrl(url)
    if index is None: return getErrorPage("Page not found")
    page = navbars[lang][index]
    return render_template(page.template,
            navbar=navbars[lang],
            active=index,
            lang=lang,
            **kwargs)

# social media tab is defined explicitly because of the extra data it needs
#@app.route("/ajankohtaista")
#@app.route("/socialmedia")
#def getSocialMediaPage():
#    try:
#        file = open("instagram_media.json", "r")
#        media = json.loads(file.read())
#    except FileNotFoundError as err:
#        return getErrorPage(str(err))
#    url = request.url_rule.rule[1:] # requested url without the leading slash
#    return getPage(url, media=media)
