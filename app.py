from flask import Flask, request, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/api")
def index():
    return "The URL for this page is {}".format(url_for("index"))


@app.route("/api/translate", methods=["GET"])
def api_translate():
    text = request.args.get("text")
    lang_from = request.args.get("lang_from")
    lang_to = request.args.get("lang_to")

    return {
        "text": translate(text, lang_from, lang_to)
    }


def translate(text, lang_from, lang_to):
    return str(text), str(lang_from), str(lang_to)
    ...
