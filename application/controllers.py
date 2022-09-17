from flask import Flask
from flask import render_template
from flask import current_app as app
from application import tasks
from datetime import datetime

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

# Test
@app.route("/hello/<msg>")
def hello(msg):
    job = tasks.just_say_hello.delay(msg)
    result = job.wait()
    return str(result), 200

@app.route("/time")
def time():
    now = datetime.now()
    print("now in flask=", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time=", dt_string)
    job = tasks.print_current_time.apply_async(countdown=10)
    result = job.wait()
    return result, 200