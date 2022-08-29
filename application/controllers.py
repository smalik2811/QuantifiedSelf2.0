from flask import Flask, request
from flask import render_template
from flask import current_app as app

@app.route("/")
def home():
    return render_template("main.html")
