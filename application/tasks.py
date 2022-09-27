from fileinput import filename
from application.workers import celery
from datetime import datetime, date
from celery.schedules import crontab
import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from application.models import User,Tracker,Log, MonthHistroy
from application.database import db
from application.config import LocalDevelopmentConfig
from jinja2 import Template
from weasyprint import HTML, CSS
import uuid
from dateutil.relativedelta import relativedelta
from email.mime.base import MIMEBase


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
    print(file_path)
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
        logsall = db.session.query(Log).filter(Log.tracker_id == tracker.tracker_id).all()
        for log in logsall:
            logs.append(log)
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
    message = template.render(user = user, misc = misc, trackers = trackers, logs = logs)
    html = HTML(string = message)
    file_name = str(uuid.uuid4()) + ".pdf"
    file_path = file_path.replace("report.html", file_name)
    print(file_path)
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
    sender.add_periodic_task(crontab(day_of_month=1, hour=0), generate_report_send_mail.s(), name = 'Send Monthly Report')