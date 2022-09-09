from flask import Flask, request
from flask import render_template
from flask import current_app as app

@app.route("/")
def login():
    return render_template("home.html")

@app.route("/login")
def home():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/tracker/create")
def createTracker():
    return render_template("createTracker.html")

@app.route("/tracker/update/<name>")
def updateTracker(name):
    return render_template("updateTracker.html")

@app.route("/log/<string:name>")
def createLog(name):
    return render_template("createLog.html")
