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

@app.route("/tracker/update/<int:id>")
def updateTracker(id):
    return render_template("updateTracker.html")

@app.route("/log/<int:id>")
def createLog(id):
    return render_template("createLog.html")

@app.route("/summary/<int:id>")
def summary(id):
    return render_template("summary.html")

@app.route("/log/update/<int:id>")
def updateLog(id):
    return render_template("updateLog.html")