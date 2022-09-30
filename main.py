import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application import workers
from application.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import User, Role
from flask_caching import Cache
from datetime import datetime
from flask_login import current_user
from flask_restful import (Resource, fields, marshal_with,
                           reqparse)
from flask_security import auth_required
from datetime import datetime
from application.database import db
from application.models import *

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
      broker_url = app.config["CELERY_BROKER_URL"],
      result_backend = app.config["CELERY_RESULT_BACKEND"],
      enable_utc = False,
      timezone = "Asia/Calcutta"
    )
    celery.Task = workers.ContextTask
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    cache = Cache(app)
    app.app_context().push()
    return app, api, celery, cache

app, api, celery , cache = create_app()



# Parser for User
user_details_parser = reqparse.RequestParser()
user_details_parser.add_argument('email', required = True)
user_details_parser.add_argument('password', required = True)
user_details_parser.add_argument('firstName', required = True)
user_details_parser.add_argument('lastName')

user_details = {
    'first_name' : fields.String,
    'last_name' : fields.String,
    'email':    fields.String,
    'id': fields.Integer
}

log_details = {
    'id': fields.Integer,
    'value' : fields.String,
    'note' : fields.String,
    'timestamp': fields.String,
    'tracker_id': fields.Integer
}


# Parser for Tracker
tracker_details_parser = reqparse.RequestParser()
tracker_details_parser.add_argument('id', type=int)
tracker_details_parser.add_argument('name', required = True)
tracker_details_parser.add_argument('description')
tracker_details_parser.add_argument('type', type=int, required = True)
tracker_details_parser.add_argument('options', action='append')

# Parser for Log
log_details_parser = reqparse.RequestParser()
log_details_parser.add_argument('value', required = True)
log_details_parser.add_argument('note')
log_details_parser.add_argument('timestamp', required = True)
log_details_parser.add_argument('trackerid', location='headers', required = True)

log_details_parser2 = reqparse.RequestParser()
log_details_parser2.add_argument('trackerid', location='headers', required = True)

log_details_parser3 = reqparse.RequestParser()
log_details_parser3.add_argument('value', required = True)
log_details_parser3.add_argument('note')
log_details_parser3.add_argument('timestamp', required = True)

@cache.memoize(timeout = 100)
def getUser(current_user):
    try:
      user = db.session.query(User).filter(User.id == current_user.id).first()
      return user, 200
    except:
        return "Unexpected error", 500

@cache.memoize(timeout = 100)
def getTrackers(current_user):
    try:
        trackers = db.session.query(Tracker).filter(Tracker.user_id == current_user.id).all()
        tracker_list = []
        for tracker in trackers:
            tracker_list.append({'id': tracker.id, 'name' : tracker.name, 'description' : tracker.description, 'last_modified' : tracker.last_modified})
        return tracker_list, 200
    except:
        return "Unexpected error", 500

@cache.memoize(timeout = 100)
def getTracker(current_user,id):
    try:
        if not id:
            return "Invalid id supplied", 400   
        tracker = db.session.query(Tracker).filter(Tracker.id == id and Tracker.user_id == current_user.id).first()
        if not tracker:
            return "Tracker not found", 404
        options_list = []
        options = db.session.query(Options).filter(Options.tracker_id == tracker.id).all()
        for option in options:
            options_list.append(option.name)
        tracker_dict = {
            'id' : tracker.id,
            'name' : tracker.name,
            'description' : tracker.description,
            'type' : tracker.type,
            'options' : options_list
        }

        return tracker_dict, 200
    except: 
        return "Unexpected error", 500

@cache.memoize(timeout = 100)
def getLogs(current_user, tracker_id):
    try: 
        tracker = db.session.query(Tracker).filter((Tracker.id == tracker_id) and (Tracker.user_id == current_user.id)).first()
        if not tracker:
            return "Tracker not found.", 404
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d At %H:%M:%S")
        tracker.last_modified = dt_string
        db.session.commit()
        logs = db.session.query(Log).filter(Log.tracker_id == tracker_id).all()
        log_list = []
        for log in logs:
            log_list.append({'id': log.id, 'value' : log.value, 'note' : log.note, 'timestamp': log.timestamp})
        return log_list, 200
    except:
        return "Unexpected error.", 500

@cache.memoize(timeout = 100)
def getLog(current_user, id):
    try:
        log = db.session.query(Log).filter(Log.id == id).first()
        if not log:
            return "Log not found", 404
        tracker = db.session.query((Tracker.id == log.tracker_id) and (Tracker.user_id == current_user.id)).first()
        if not tracker:
            return "You are not authorised", 401
        return log, 200    
    except:
        return "Unexpected error", 500


class UserAPI(Resource):

    def post(self):
        args = user_details_parser.parse_args()        
        email = args.get("email")
        password = args.get("password")
        firstName = args.get("firstName")
        lastName = args.get("lastName")

        if "@" in email:
            pass
        else:
            return "Provide valid email", 400

        user = db.session.query(User).filter(User.email == email).first()
        if user:
            return "Email already exist.", 409

        try:
            new_user = User(email=email, password=password, first_name=firstName, last_name=lastName, fs_uniquifier=email, active=1, role=1)
            db.session.add(new_user)
            db.session.commit()
            return "User created successfully.", 201
        except:
            return "Unexpected error.", 500
            
    @auth_required("token")
    @marshal_with(user_details)
    def get(self):
        return getUser(current_user)

class Tracker1API(Resource):
    
    @auth_required('token')
    def post(self):
        try:
            args = tracker_details_parser.parse_args()
            name = args.get('name')
            description = args.get('description')
            type = args.get('type')
            options = args.get('options')
            
            if db.session.query(Tracker).filter((Tracker.name == name) and (Tracker.user_id == current_user.id)).first():
                return "Tracker already exist", 409
            
            if not 0 < int(type) < 5 : 
                return "Invalid Tracker Type supplied", 400
            
            new_tracker = Tracker(name = name, description = description, type = type, user_id = current_user.id, last_modified = "Never")
            db.session.add(new_tracker)
            db.session.commit()

            new_tracker = db.session.query(Tracker).filter(Tracker.name == name).first()

            if new_tracker:
                if int(type) == 3:
                    new_option = Options(tracker_id = new_tracker.id, name = "true", active = 1)
                    db.session.add(new_option)
                    new_option = Options(tracker_id = new_tracker.id, name = "false", active = 1)
                    db.session.add(new_option)
                elif int(type) == 4:
                    for option in options:
                        new_option = Options(tracker_id = new_tracker.id, name = option, active = 1)
                        db.session.add(new_option)
                new_histroy = MonthHistroy(tracker_id = new_tracker.id)
                db.session.add(new_histroy)
                db.session.commit()
            else:
                return "Unexpected error", 500
            cache.delete_memoized(getTracker,current_user, id)
            cache.delete_memoized(getTrackers,current_user)
            return "Tracker created Successfuly", 201
        except:
            new_tracker = db.session.query(Tracker).filter(Tracker.name == name).first()
            if new_tracker:
                db.session.delete(new_tracker)
                db.session.commit()
            return "Unexpected error", 500
    
    @auth_required('token')
    def get(self):
        return getTrackers(current_user)

class Tracker2API(Resource):
    
    @auth_required('token')
    def get(self, id):  
        return getTracker(current_user, id)

    @auth_required("token")
    def patch(self, id):
        try:
            args = tracker_details_parser.parse_args()
            id = tracker_details_parser.get('id')  
            if not id:
                return "Invalid id supplied", 400
            new_name = args.get("name")
            new_description = args.get("description")
            new_options = args.get("options")
            tracker = db.session.query(Tracker).filter(Tracker.id == id).first()
            if not tracker:
                return "Tracker not found.", 404
            
            same_tracker = db.session.query(Tracker).filter((Tracker.name == new_name) and (Tracker.user_id == current_user.id)).first() 
            if same_tracker:
                return "Tracker with the name already exist.", 400
            tracker.name = new_name
            tracker.description = new_description

            if tracker.type == 4:
                options = db.session.query(Options).filter(Options.tracker_id == id)
                for option in options:
                    option.active = 0
                for option in new_options:
                    old_option = db.session.query(Options).filter((Options.tracker_id == id) and (Options.name == options)).first()
                    if old_option:
                        old_option.active = 1
                    else:
                        new_option = Options(tracker_id = id, name = options, active = 1)
                        db.session.add(new_option)
            db.session.commit()
            cache.delete_memoized(getTracker,current_user, id)
            cache.delete_memoized(getTrackers,current_user)
            return "Update Successful", 201
        except:
            return "Unexpected error", 500   


    @auth_required("token")
    def delete(self, id):
        try:
            if not id:
                return "Invalid id supplied", 400
            tracker = db.session.query(Tracker).filter(Tracker.id == id and Tracker.user_id == current_user.id).first()
            if not tracker:
                return "Tracker not found.", 404
            db.session.delete(tracker)
            db.session.commit()
            cache.delete_memoized(getTracker,current_user, id)
            cache.delete_memoized(getTrackers,current_user)
            return "Deletion Successful", 200
        except:
            return "Unexpected error", 500      

class Log1API(Resource):

    @auth_required('token')
    def post(self):
        try:
            args = log_details_parser.parse_args()
            tracker_id = args.get('trackerid')    
            value = args.get("value")
            note = args.get("note")
            timestamp = args.get("timestamp")
            
            tracker = db.session.query(Tracker).filter((Tracker.id == tracker_id) and (Tracker.user_id == current_user.id)).first()
            if not tracker:
                return "Tracker not found.", 404
            new_log = Log(tracker_id = tracker_id, value = value, note = note, timestamp = timestamp)
            db.session.add(new_log)
            db.session.commit()
            cache.delete_memoized(getLogs,current_user)
            return "Log created successfully.", 201
        except:
            return "Unexpected error.", 500

    @auth_required('token')
    def get(self):
        args = log_details_parser2.parse_args()
        tracker_id = args.get('trackerid') 
        return getLogs(current_user, tracker_id)

class Log2API(Resource):

    @auth_required('token')
    @marshal_with(log_details)
    def get(self, id):
        return getLog(current_user, id)

    @auth_required('token')
    def patch(self, id):
        try:
            args = log_details_parser3.parse_args()        
            new_value = args.get("value")
            new_note = args.get("note")
            new_timestamp = args.get("timestamp")

            log = db.session.query(Log).filter(Log.id == id).first()
            if not log:
                return "Log not found", 404
            tracker = db.session.query(Tracker).filter((Tracker.id == log.tracker_id) and (Tracker.user_id == current_user.id)).first()
            if not tracker:
                return "You are not authorised", 401
            
            log.value = new_value
            log.note = new_note
            log.timestamp = new_timestamp
            db.session.commit()
            cache.delete_memoized(getLog,current_user, id)
            cache.delete_memoized(getLogs,current_user)
            return "Update Successful", 201
        except:
            return "Unexpected error", 500

    @auth_required('token')
    def delete(self, id):
        try:
            if not id:
                return "Invalid id supplied", 400
            log = db.session.query(Log).filter(Log.id == id).first()
            if not log:
                return "Log not found", 404
            tracker = db.session.query(Tracker).filter((Tracker.id == log.tracker_id) and (Tracker.user_id == current_user.id)).first()
            if not tracker:
                return "You are not authorised", 401
            db.session.delete(log)
            db.session.commit()
            cache.delete_memoized(getLog,current_user, id)
            cache.delete_memoized(getLogs,current_user)
            return "Deletion Successful", 200
        except:
            return "Unexpected error", 500       


# Import all the controllers so they are loaded
from application.controllers import *

# Add all restful controllers
# from application.api import UserAPI, Tracker1API, Tracker2API, Log1API, Log2API
api.add_resource(UserAPI, "/api/user")
api.add_resource(Tracker2API,"/api/tracker/<int:id>")
api.add_resource(Tracker1API, "/api/tracker")
api.add_resource(Log1API, "/api/log")
api.add_resource(Log2API, "/api/log/<int:id>")

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)