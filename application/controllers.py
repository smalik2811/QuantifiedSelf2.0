from flask import Flask, request
from flask import render_template
from flask import current_app as app

@app.route("/")
def login():
    return render_template("home.html")

@app.route("/login")
def home():
    return render_template("login.html")
