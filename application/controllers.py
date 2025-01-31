from flask import Flask
from flask import render_template, send_file, request
from flask import current_app as app
from application import tasks
import os

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

@app.route("/logs/export/<int:id>")
def exportLogs(id):
    try:
        job = tasks.export_logs.delay(id)
        file = job.wait()
        return send_file(file, attachment_filename = "Logs-"+(str(id) + ".csv"))
    except Exception as e:
        return str(e)

@app.route("/log/export/<int:id>")
def exportLog(id):
    try:
        job = tasks.export_log.delay(id)
        file = job.wait()
        return send_file(file, attachment_filename = "Log-"+(str(id) + ".csv"))
    except Exception as e:
        return str(e)

@app.route("/trackers/export/<int:id>")
def exportTrackers(id):
    try:
        job = tasks.export_trackers.delay(id)
        file = job.wait()
        return send_file(file, attachment_filename = "Tracker-"+(str(id) + ".csv"))
    except Exception as e:
        return str(e)

@app.route("/logs/import/<int:id>", methods = ['POST'])
def uploadLog(id):
    if request.method == 'POST':
        file = request.files['file']
        path = os.path.realpath(__file__).replace("application", "temp")
        path = path[:-8] + file.filename
        file.save(path)
        tasks.import_log.delay(path = path, tracker_id = id)
    return home()

@app.route("/trackers/import/<int:id>",methods= ['POST'])
def uploadTracker(id):
    if request.method == 'POST':
        file = request.files['file']
        path = os.path.realpath(__file__).replace("application", "temp")
        path = path[:-8] + file.filename
        file.save(path)
        tasks.import_tracker.delay(path = path, user_id = id)
    return home()

# Test
@app.route("/hello/<msg>")
def hello(msg):
    job = tasks.just_say_hello.delay(msg)
    result = job.wait()
    return str(result), 200

@app.route("/mail")
def mail():
    tasks.generate_report_send_mail()
    return "OK",200

@app.route("/report")
def report():
    tasks.delete_files()
    return "OK",200