from flask import *
from app import app

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/2")
def homepage2():
    return render_template("homepage2.html")

@app.route("/preview")
def preview():
    return render_template("preview.html")

@app.route("/preview2")
def preview2():
    return render_template("preview2.html")