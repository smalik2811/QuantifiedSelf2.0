from datetime import datetime
from flask import current_app as app
import json
from flask_login import current_user
from flask_restful import (Resource, fields, marshal_with,
                           reqparse)
from flask_security import auth_required
from datetime import datetime

from application.database import db
from application.models import *

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
    'password': fields.String
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

class User1API(Resource):

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
        try:
            return current_user, 200
        except:
            return "Unexpected error", 500
    
    @auth_required("token")
    def patch(self):
        try:
            args = user_details_parser.parse_args()        
            email = args.get("email")
            password = args.get("password")
            firstName = args.get("firstName")
            lastName = args.get("lastName")

            user = db.session.query(User).filter(User.email == email).first()
            if user:
                return "Email already exist.", 409
            
            logged_user = db.session.query(User).filter(User.email == current_user.email).first()

            logged_user.email = email
            logged_user.password = password
            logged_user.first_name = firstName
            logged_user.last_name = lastName
            
            db.session.commit()

            return "Update Successful", 201
        except:
            return "Unexpected error", 500
        
    @auth_required("token")
    def delete(self):
        try:
            logged_user = db.session.query(User).filter(User.email == current_user.email).first()
            db.session.delete(logged_user)
            db.session.commit()
            return "Deletion Successful", 200
        except:
            return "Unexpected error", 500

class User2API(Resource):
    def get(self):
        try:
            usersobj = []
            now = datetime.now()
            Users = db.session.query(User)
            for user in Users:
                tracker = db.session.query(Tracker).filter(Tracker.user_id == User.id).order_by(Tracker.last_modified.desc()).first()
                dt_string = now.strftime("%Y-%m-%d")
                print("Current date:", dt_string)
                print("Last modified:", tracker.last_modified[0:10])
                if dt_string != tracker.last_modified[0:10]:
                    userobj = {"firstname": "", "lastname": ""}
                    userobj["firstname"] = user.first_name
                    userobj["lastname"] = user.last_name
                    usersobj+= userobj
            return json.dumps(usersobj), 200
        except:
            return "Unexpected error", 500

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
            
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d At %H:%M:%S")
            new_tracker = Tracker(name = name, description = description, type = type, user_id = current_user.id, last_modified = dt_string)
            db.session.add(new_tracker)
            db.session.commit()

            new_tracker = db.session.query(Tracker).filter(Tracker.name == name).first()

            if new_tracker:
                if int(type) == 3:
                    new_option = Options(tracker_id = new_tracker.id, name = "True", active = 1)
                    db.session.add(new_option)
                    new_option = Options(tracker_id = new_tracker.id, name = "False", active = 1)
                    db.session.add(new_option)
                elif int(type) == 4:
                    for option in options:
                        new_option = Options(tracker_id = new_tracker.id, name = option, active = 1)
                        db.session.add(new_option)
                db.session.commit()
            else:
                return "Unexpected error", 500
            return "Tracker created Successfuly", 201
        except:
            new_tracker = db.session.query(Tracker).filter(Tracker.name == name).first()
            if new_tracker:
                db.session.delete(new_tracker)
                db.session.commit()
            return "Unexpected error", 500
    
    @auth_required('token')
    def get(self):
        try:
            trackers = db.session.query(Tracker).filter(Tracker.user_id == current_user.id).all()
            tracker_list = []
            for tracker in trackers:
                tracker_list.append({'id': tracker.id, 'name' : tracker.name, 'description' : tracker.description, 'last_modified' : tracker.last_modified})
            return tracker_list, 200
        except:
            return "Unexpected error", 500  

class Tracker2API(Resource):
    
    @auth_required('token')
    def get(self, id):
        try:
            if not id:
                return "Invalid id supplied", 400   
            tracker = db.session.query(Tracker).filter(Tracker.id == id).first()
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
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d At %H:%M:%S")
            tracker.name = new_name
            tracker.description = new_description
            tracker.last_modified = dt_string

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

            return "Update Successful", 201
        except:
            return "Unexpected error", 500   


    @auth_required("token")
    def delete(self, id):
        try:
            if not id:
                return "Invalid id supplied", 400
            tracker = db.session.query(Tracker).filter(Tracker.id == id).first()
            if not tracker:
                return "Tracker not found.", 404
            db.session.delete(tracker)
            db.session.commit()
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
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d At %H:%M:%S")
            tracker.last_modified = dt_string
            db.session.commit()
            return "Log created successfully.", 201
        except:
            return "Unexpected error.", 500

    @auth_required('token')
    def get(self):
        try:
            args = log_details_parser2.parse_args()
            tracker_id = args.get('trackerid')  
            tracker = db.session.query(Tracker).filter((Tracker.id == tracker_id) and (Tracker.user_id == current_user.id)).first()
            if not tracker:
                return "Tracker not found.", 404
            logs = db.session.query(Log).filter(Log.tracker_id == tracker_id).all()
            log_list = []
            for log in logs:
                log_list.append({'id': log.id, 'value' : log.value, 'note' : log.note, 'timestamp': log.timestamp})
            return log_list, 200
        except:
            return "Unexpected error.", 500

class Log2API(Resource):

    @auth_required('token')
    @marshal_with(log_details)
    def get(self, id):
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
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d At %H:%M:%S")
            tracker.last_modified = dt_string        
            db.session.commit()
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
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d At %H:%M:%S")
            tracker.last_modified = dt_string
            db.session.commit()
            return "Deletion Successful", 200
        except:
            return "Unexpected error", 500       
