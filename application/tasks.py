from application.workers import celery
from datetime import datetime
from celery.schedules import crontab

@celery.task()
def just_say_hello(name):
    print("INSIDE TASK")
    print("HELLO {}".format(name))
    return "HELLO {}".format(name)

@celery.task()
def print_current_time():
    print("START")
    now = datetime.now()
    print("now in task=", now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time=", dt_string)
    print("COMPLETE") 
    return dt_string

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=0, day_of_week = "*"), print_current_time.s(), name = 'At every 10 seconds')