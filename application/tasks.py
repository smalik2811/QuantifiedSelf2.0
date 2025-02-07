from application.workers import celery
from datetime import datetime, date
from celery.schedules import crontab
import requests
import json
import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from application.models import User,Tracker,Log, MonthHistroy, Options
from application.database import db
from application.config import LocalDevelopmentConfig
from jinja2 import Template
from weasyprint import HTML, CSS
import uuid
from dateutil.relativedelta import relativedelta
from email.mime.base import MIMEBase
from dateutil.parser import parse
import re


@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print("HELLO {}".format(name))
    return "HELLO {}".format(name)

@celery.task()
def send_alert():
    user_list = []
    try:
        now = datetime.now()
        Users = db.session.query(User).all()
        for user in Users:
            tracker = db.session.query(Tracker).filter(Tracker.user_id == user.id).order_by(Tracker.last_modified.desc()).first()
            if tracker:
                log = db.session.query(Log).filter(Log.tracker_id == tracker.id).order_by(Log.timestamp.desc()).first()
                dt_string = now.strftime("%Y-%m-%d")
                if dt_string != log.timestamp[0:10]:
                    user_list.append({'firstname': user.first_name, 'lastname': user.last_name})
            else:
                user_list.append({'firstname': user.first_name, 'lastname': user.last_name}) 
    except:
        print("Something went wrong")
    for user in user_list:
        text = "Hi {} {}, Looks like you haven't logged your trackers today.".format(user["firstname"], user["lastname"])
        data = {"text": text}
        post_webhook(data)

@celery.task()
def post_webhook(data):
    requests.post(LocalDevelopmentConfig.CHAT_WEBHOOK_URL,
    data=json.dumps(data), 
    headers={'content-type': 'application/json'})


@celery.on_after_finalize.connect
def alert(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17, minute=0, day_of_week = "*"), send_alert.s(), name = 'Send alert every evening to log')
    sender.add_periodic_task(crontab(minute="*", hour=11), generate_report.s(), name = 'Send Monthly Report')

@celery.task()
def send_mail(receiver_address, subject, message, attachment_file = None):
    msg = MIMEMultipart()
    msg['From'] = LocalDevelopmentConfig.SENDER_ADDRESS
    msg['To'] = receiver_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, "html"))
     
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content_Disposition", f"attachment; filename= {attachment_file}",
            )
        msg.attach(part)

    s = smtplib.SMTP(host = LocalDevelopmentConfig.SMTP_SERVER_HOST, port = LocalDevelopmentConfig.SMTP_SERVER_PORT)
    s.login(LocalDevelopmentConfig.SENDER_ADDRESS, LocalDevelopmentConfig.SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    os.remove(attachment_file)
    return True

@celery.task()
def generate_report(user):
    path = os.path.realpath(__file__).replace("application", "report")
    path = path.split("/")
    path = path[:-1]
    file_path = ""
    for x in path:
        file_path = file_path + "/" + x
    file_path = file_path[1:] + "/report.html"
    with open(file_path) as file_:
        template = Template(file_.read())
    misc = {
        'numcount': 0,
        'boolcount': 0,
        'durcount': 0,
        'multicount': 0, 
        'newcount': 0, 
        'month': (date.today() - relativedelta(months=1)).strftime("%B"),
        'numtrackers': "",
        'booltrackers': "",
        'durtrackers': "",
        'multitrackers': "",
        }
    all_trackers = db.session.query(MonthHistroy).all()
    trackers = []
    logs = []
    for tracker in all_trackers:
        trackers.append(db.session.query(Tracker).filter(Tracker.id == tracker.tracker_id and Tracker.user_id == user.id).first())
    for tracker in trackers:
        misc['newcount'] += 1
        type = tracker.type
        if type == 1:
            misc['numcount'] += 1
            misc['numtrackers'] = misc['numtrackers'] + tracker.name + ","
        elif type == 2:
            misc['durcount'] += 1
            misc['durtrackers'] = misc['durtrackers'] + tracker.name + ","
        elif type == 3:
            misc['boolcount'] += 1
            misc['booltrackers'] = misc['booltrackers'] + tracker.name + ","
        elif type == 4:
            misc['multicount'] += 1
            misc['multitrackers'] = misc['multitrackers'] + tracker.name + ","
    trackers = []
    all_trackers = db.session.query(Tracker).filter(Tracker.user_id == user.id).all()
    for tracker in all_trackers:
        trackers.append(tracker)
        logsall = db.session.query(Log).filter(Log.tracker_id == tracker.id and Log.timestamp[5:7] == (int(str(date.today())[5:7])-1)).all()
        for log in logsall:
            logs.append(log)
    message = template.render(user = user, misc = misc, trackers = trackers, logs = logs)
    html = HTML(string = message)
    file_name = str(uuid.uuid4()) + ".pdf"
    file_path = file_path.replace("report.html", file_name)
    css = CSS(filename = file_path.replace(file_name, "report.css"))
    html.write_pdf(target = file_path, stylesheets=[css])
    return file_path
    

@celery.task()
def generate_report_send_mail():
    path = os.path.realpath(__file__).replace("application", "templates")
    path = path.split("/")
    path = path[:-1]
    file_path = ""
    for x in path:
        file_path = file_path + "/" + x
    file_path = file_path[1:] + "/monthly_report.html"
    # For each individual create the report and mail it.
    users = db.session.query(User).all()
    for user in users:
        #Generate the report here
        with open(file_path) as file_:
            template = Template(file_.read())
            message = template.render(data = user)
        report = generate_report(user = user)
        subject = "Monthly Report"

        send_mail(receiver_address = user.email, subject = subject, message = message, attachment_file=report)
    db.session.query(MonthHistroy).delete()
    db.session.commit()

@celery.on_after_finalize.connect
def report(sender, **kwargs):
    sender.add_periodic_task(crontab(day_of_month=1, hour=0, minute=0), generate_report_send_mail.s(), name = 'Send Monthly Report')

@celery.task()
def export_logs(id):
    logs = db.session.query(Log).filter(Log.tracker_id == id).all()
    path = os.path.realpath(__file__).replace("application", "temp")
    path = path[:-8] + str(uuid.uuid4()) + ".csv"
    file = open(path, 'w')
    writer = csv.writer(file)
    header = ['timestamp', 'value', 'note']
    writer.writerow(header)
    for log in logs:
        writer.writerow([log.timestamp, log.value, log.note])
    file.close()
    return path

@celery.task()
def export_trackers(id):
    trackers = db.session.query(Tracker).filter(Tracker.user_id == id).all()
    path = os.path.realpath(__file__).replace("application", "temp")
    path = path[:-8] + str(uuid.uuid4()) + ".csv"
    file = open(path, "w")
    writer = csv.writer(file)
    header = ['name', 'description', 'type', 'options']
    writer.writerow(header)

    for tracker in trackers:
        opt_str = ""
        if tracker.type == 3 or tracker.type == 4:
            options = db.session.query(Options).filter(Options.tracker_id == tracker.id and Options.active == 1).all()
            for option in options:
                opt_str = opt_str + option.name + "*"
            opt_str = opt_str[:-1]
        data = [tracker.name, tracker.description, tracker.type, opt_str]
        writer.writerow(data)
    file.close()
    return path

@celery.task()
def export_log(id):
    log = db.session.query(Log).filter(Log.id == id).first()
    path = os.path.realpath(__file__).replace("application", "temp")
    path = path[:-8] + str(uuid.uuid4()) + ".csv"
    file = open(path, 'w')
    writer = csv.writer(file)
    header = ['timestamp', 'value', 'note']
    writer.writerow(header)
    writer.writerow([log.timestamp, log.value, log.note])
    file.close()
    return path

@celery.task()
def import_log(path, tracker_id):
    tracker = db.session.query(Tracker).filter(Tracker.id == tracker_id).first()
    if tracker:
        file = open(path, 'r')
        reader = csv.reader(file)
        fields = next(reader)
        for row in reader:
            if not len(row) == 3:
                continue
            if not is_date(row[0]):
                continue
            if (tracker.type == 1 or tracker.type == 2) and str.isdigit(row[1]):
                addLog(tracker_id,row)
            if (tracker.type == 3 and (row[1]=="true" or row[1] == "false")):
                addLog(tracker_id,row)
            if tracker.type == 4:
                options = db.session.query(Options).filter(Options.tracker_id == tracker_id and Options.active == 1)
                active_options = []
                for option in options:
                    active_options.append(option.name)
                if row[1] in active_options:
                    addLog(tracker_id, row)
        os.remove(path)

def addLog(tracker_id, row):
    log = Log(tracker_id = tracker_id, value = row[1], note = row[2], timestamp = row[0])
    db.session.add(log)
    db.session.commit()

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        dateRegex = re.compile(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d')
        date_str = dateRegex.search(string)
        if date_str is None:
            return False
        date_str = str(date_str.group())
        if len(string) == len(date_str):
            return True
        else:
            return False
    except ValueError:
        return False

@celery.task()
def import_tracker(path, user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user:
        file = open(path, 'r')
        reader = csv.reader(file)
        fields = next(reader)
        for row in reader:
            if not len(row) == 4:
                continue
            if  1 <= int(row[2]) <= 4:
                try:
                    tracker = db.session.query(Tracker).filter(Tracker.name == row[0] and Tracker.user_id == user_id).first()
                    if tracker:
                        continue
                    tracker = Tracker(name = row[0], description = row[1], type = int(row[2]), user_id = user_id, last_modified = "Never")
                    db.session.add(tracker)
                    db.session.commit()
                except:
                    continue
                tracker = db.session.query(Tracker).filter(Tracker.name == row[0] and Tracker.user_id == user_id).first()
                if tracker:
                    if tracker.type == 3:
                        option = Options(tracker_id = tracker.id, name = "true", active = 1)
                        db.session.add(option)
                        db.session.commit()
                        option = Options(tracker_id = tracker.id, name = "false", active = 1)
                        db.session.add(option)
                        db.session.commit()
                    if tracker.type == 4:
                        opt_list = row[3].split("*")
                        if len(opt) == 0:
                            db.session.delete(tracker)
                            db.session.commit()
                            continue
                        for opt in opt_list:
                            option = Options(tracker_id = tracker.id, name = opt, active = 1)
                            db.session.add(option)
                            db.session.commit()
        os.remove(path)

@celery.task()
def delete_files():
    path = os.path.realpath(__file__).replace("application", "temp")
    path = path[:-9]
    files = os.listdir(path)
    for file in files:
        if os.path.exists(path):
            os.remove(path + "/" + file)

@celery.on_after_finalize.connect
def scheduled_delete_files(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0, minute=0), generate_report_send_mail.s(), name = 'Delete Unwanted files')