from application.workers import celery
from datetime import datetime
from celery.schedules import crontab
import requests
import json
from application.models import User,Tracker,Log
from application.database import db
from application.config import LocalDevelopmentConfig

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
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17, minute=0, day_of_week = "*"), send_alert.s(), name = 'Send alert every evening to log')