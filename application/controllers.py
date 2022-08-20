from flask import Flask, request
from flask import render_template
from flask import current_app as app

@app.route("/", methods=["GET", "POST"])
def articles():
    return "Hello World"
