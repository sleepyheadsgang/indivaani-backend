from utils import translator
from utils.htmlhandler import HTMLTranslator
from flask import Flask, request, url_for, send_file

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
        "text": translator.translate(text, lang_from, lang_to)
    }

@app.route("/api/translate-file", methods=["POST"])
def api_translate_file():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    
    file = request.files.get("file")
    lang_from = request.form.get("lang_from")
    lang_to = request.form.get("lang_to")

    if not file:
        return {
            "error": "No file uploaded"
        }

    # Perform translation on the file
    translator = HTMLTranslator(file, lang_from, lang_to)
    translated_file = translator.translate_html()

    # return app.response_class(
    #     response=translated_text,
    #     status=200,
    #     mimetype='text/html'
    # )

    return send_file(translated_file, mimetype="text/html", as_attachment=True, attachment_filename="translated.html")
