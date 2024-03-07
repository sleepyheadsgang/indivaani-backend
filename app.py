import datetime
import json
import os
import random
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from utils.htmlhandler import HTMLTranslator
from utils import translator, audiohandler
from flask import Flask, flash, redirect, request, url_for, send_file, render_template


app = Flask(__name__, template_folder="static/uploads")
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(os.getcwd(), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')

db = SQLAlchemy(app)
app.app_context().push()


class Translations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), nullable=False)
    original_text = db.Column(db.String(1000), nullable=False)
    translated_text = db.Column(db.String(1000), nullable=False)
    from_lang = db.Column(db.String(10), nullable=True)
    to_lang = db.Column(db.String(10), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)


@app.route("/")
@app.route("/api")
def index():
    return "The URL for this page is {}".format(url_for("index")) + """
    <h2>Normal Translation</h2>
    <form method="POST" action="/api/translate">
        <input type="text" name="text" placeholder="Enter text to translate">
        <input type="text" name="lang_from" placeholder="Enter language to translate from">
        <input type="text" name="lang_to" placeholder="Enter language to translate to">
        <input type="text" name="user_id" placeholder="Enter user id">
        <input type="submit" value="Translate">
    </form>
    <h2>Translation History</h2>
    <form method="POST" action="/api/translate-history">
        <input type="text" name="user_id" placeholder="Enter user id">
        <input type="submit" value="Get translation history">
    </form>
    <h2>File Translation</h2>
    <form method="POST" action="/api/translate-file" enctype="multipart/form-data">
        <input type="file" name="file" id="file" accept="text/html">
        <input type="text" name="lang_from" placeholder="Enter language to translate from">
        <input type="text" name="lang_to" placeholder="Enter language to translate to">
        <input type="text" name="user_id" placeholder="Enter user id">
        <input type="submit" value="Translate">
    </form>
    <h2>Webpage Translation</h2>
    <form method="POST" action="/api/translate-webpage">
        <input type="text" name="url" placeholder="Enter webpage URL">
        <input type="text" name="lang_to" placeholder="Enter language to translate to">
        <input type="submit" value="Translate">
    </form>
    <h2>Audio Translation</h2>
    <form method="POST" action="/api/translate-audio" enctype="multipart/form-data">
        <input type="file" name="file" id="file" accept="audio/*">
        <input type="text" name="lang_to" placeholder="Enter language to translate to">
        <input type="submit" value="Translate">
    </form>
    """


@app.route("/api/translate", methods=["GET", "POST"])
def api_translate():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    text = request.form.get("text")
    lang_from = request.form.get("lang_from")
    if lang_from is not None:
        lang_from = lang_from.lower()
    lang_to = request.form.get("lang_to").lower()
    user_id = request.form.get("user_id")

    translated_text = translator.translate(text, lang_from, lang_to)
    translation = Translations(userid=user_id, original_text=text, translated_text=translated_text,
                               from_lang=lang_from, to_lang=lang_to, datetime=datetime.datetime.now())
    db.session.add(translation)
    db.session.commit()

    return {
        "text": translated_text
    }


@app.route("/api/translate-webpage", methods=["POST"])
def api_translate_webpage():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    url = request.form.get("url")
    lang_to = request.form.get("lang_to").lower()
    data = get_page(url)
    filename = f"{gen_random_seq()}.html"
    saved_fp = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(saved_fp, "w", encoding="utf-8") as file:
        file.write(data.decode("utf-8"))
    html_translator = HTMLTranslator(
        saved_fp, "en", lang_to, translator.translate)
    html_translator.translate_html()
    return redirect(url_for("get_translated_file", mypath=filename.rstrip(".html")))

def gen_random_seq(length: int=30):
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=length))

def get_page(url: str):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    return mybytes

@app.route("/preview/<mypath>", methods=["GET"])
def get_translated_file(mypath: str):
    filename = request.args.get("filename")
    print("FILENAME", filename)
    return render_template(mypath+"_translated.html")

@app.route("/api/translate-audio", methods=["POST"])
def api_translate_audio():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    file = request.files['file']
    lang_to = request.form.get("lang_to").lower()
    # If the user does not select a file, the browser submits  an
    # empty file without a filename.
    if file.filename == '' or not file:
        flash('No selected file')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    saved_fp = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(saved_fp)
    transcribed_text = audiohandler.transcribe_audio(saved_fp)
    translated_text = translator.translate(transcribed_text, "auto", lang_to)
    os.remove(saved_fp)
    return {
        "text": translated_text
    }

@app.route("/api/translate-file", methods=["POST"])
def api_translate_file():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print("File is there", file.filename)
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if not file:
        flash('No selected file')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    saved_fp = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(saved_fp)

    lang_from = request.form.get("lang_from").lower()
    lang_to = request.form.get("lang_to").lower()
    # Perform translation on the file
    html_translator = HTMLTranslator(
        saved_fp, lang_from, lang_to, translator.translate)
    translated_file = html_translator.translate_html()
    return send_file(translated_file, mimetype="text/html", as_attachment=True)


@app.route("/api/translate-history", methods=["POST"])
def api_translate_history():
    if request.method != "POST":
        return {
            "error": "Invalid request method"
        }
    user_id = request.form.get("user_id")
    translations = Translations.query.filter_by(userid=user_id).all()
    return {
        "translations": [
            {
                "original_text": translation.original_text,
                "translated_text": translation.translated_text,
                "from_lang": translation.from_lang,
                "to_lang": translation.to_lang,
                "datetime": translation.datetime
            }
            for translation in translations
        ]
    }


@app.route("/api/languages", methods=["GET"])
def get_languages():
    return json.load(open("./utils/langs.json"))


db.create_all()
