from application.workers import celery
from datetime import datetime
from celery.schedules import crontab
import requests
import json
from application.config import LocalDevelopmentConfig

@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print("HELLO {}".format(name))
    return "HELLO {}".format(name)

@celery.task()
def send_alert():
    user_list = requests.get('http://127.0.0.1:8080/api/users')
    user_list = user_list.json()
    for user in user_list:
        data = {"text": "Hi {} {}, Looks like you haven't logged your trackers today.".format(user["firstname"], user["lastname"])}
        requests.post(LocalDevelopmentConfig.CHAT_WEBHOOK_URL,
        data=json.dumps(data), 
        headers={'content-type': 'application/json'})

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=19, minute=44, day_of_week = "*"), send_alert.s(), name = 'Send alert every evening to log')