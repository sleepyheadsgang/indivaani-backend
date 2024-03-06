from flask import Flask, request, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/api")
def index():
    return "The URL for this page is {}".format(url_for("index"))


@app.route("/api/translate", methods=["POST"])
def api_translate():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    text = request.form.get("text")
    lang_from = request.form.get("lang_from")
    lang_to = request.form.get("lang_to")

    return {
        "text": translate(text, lang_from, lang_to)
    }


def translate(text, lang_from, lang_to):
    return str(text), str(lang_from), str(lang_to)
    ...
