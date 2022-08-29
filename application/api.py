from dataclasses import field
from hmac import digest_size
from math import exp
from sqlite3 import Timestamp
from urllib import request
from flask_restful import Resource, Api, request
from flask_restful import fields, marshal_with, marshal
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError, DuplicateResource
from application.models import *
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort
from flask_security import auth_required
from flask_login import current_user
from flask import jsonify

# Parser for User
user_details_parser = reqparse.RequestParser()
user_details_parser.add_argument('email', required = True)
user_details_parser.add_argument('password', required = True)
user_details_parser.add_argument('firstName', required = True)
user_details_parser.add_argument('lastName')

user_details = {
    'first_name' : fields.String,
    'last_name' : fields.String,
    'email':    fields.String
}

log_details = {
    'id': fields.Integer,
    'value' : fields.String,
    'note' : fields.String,
    'timestamp': fields.String
}


# Parser for Tracker
tracker_details_parser = reqparse.RequestParser()
tracker_details_parser.add_argument('name', required = True)
tracker_details_parser.add_argument('description')
tracker_details_parser.add_argument('type', type=int, required = True)
tracker_details_parser.add_argument('options', action='append')

# Parser for Log
log_details_parser = reqparse.RequestParser()
log_details_parser.add_argument('value', required = True)
log_details_parser.add_argument('note')
log_details_parser.add_argument('timestamp', required = True)
log_details_parser.add_argument('Tracker-Id', location='headers', required = True)

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
            raise BusinessValidationError(
                status_code=400, error_code="BE1006", error_message="Invalid email")

        user = db.session.query(User).filter(User.email == email).first()

        if user:
            raise BusinessValidationError(
                status_code=409, error_code="BE1007", error_message="email already exist.")

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

            logged_user = db.session.query(User).filter(User.email == current_user.email).first()

            logged_user.email = email
            logged_user.password = password
            logged_user.first_name = firstName
            logged_user.last_name = lastName
            
            db.session.commit()

            return "Update Successful", 200
        except:
            return "Unexpected error", 500
        
    @auth_required("token")
    def delete(self):
        try:
            logged_user = db.session.query(User).filter(User.email == current_user.email).first()
            db.session.delete(logged_user)
            db.session.commit()
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
            
            if db.session.query(Tracker).filter(Tracker.name == name).first():
                raise BusinessValidationError(409, "BE010", "Tracker already exist.")
            
            if not 0 < int(type) < 5 : 
                raise BusinessValidationError(400, "BE011", "Invalid Tracker Type")

            new_tracker = Tracker(name = name, description = description, type = type, user_id = current_user.id)
            db.session.add(new_tracker)
            db.session.commit()

            new_tracker = db.session.query(Tracker).filter(Tracker.name == name).first()

            if new_tracker:
                if int(type) == 3:
                    new_option = Options(tracker_id = new_tracker.id, name = "True")
                    db.session.add(new_option)
                    new_option = Options(tracker_id = new_tracker.id, name = "False")
                    db.session.add(new_option)
                elif int(type) == 4:
                    for option in options:
                        new_option = Options(tracker_id = new_tracker.id, name = option)
                        db.session.add(new_option)
                db.session.commit()
            else:
                return "Unexpected error", 500
            return "Tracker created Successfuly", 201
        except:
            return "Unexpected error", 500
    
    @auth_required('token')
    def get(self):
        trackers = db.session.query(Tracker).filter(Tracker.user_id == current_user.id).all()
        tracker_list = []
        for tracker in trackers:
            tracker_list.append({'id': tracker.id, 'name' : tracker.name, 'description' : tracker.description})
        return tracker_list, 200

class Tracker2API(Resource):
    
    @auth_required('token')
    def get(self, name):

        tracker = db.session.query(Tracker).filter(Tracker.name == name).first()
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

    @auth_required("token")
    def patch(self, name):
        try:
            args = tracker_details_parser.parse_args()        
            new_name = args.get("name", None)
            new_description = args.get("description")
            new_options = args.get("options", None)

            tracker = db.session.query(Tracker).filter(Tracker.name == name).first()

            if new_name:
                tracker.name = new_name
            
            tracker.description = new_description
                        
            db.session.commit()

            return "Update Successful", 200
        except:
            return "Unexpected error", 500   


    @auth_required("token")
    def delete(self, name):
        try:
            tracker = db.session.query(Tracker).filter(Tracker.name == name).first()
            db.session.delete(tracker)
            db.session.commit()
            return "Deletion Successful", 200
        except:
            return "Unexpected error", 500      

class Log1API(Resource):

    @auth_required('token')
    def post(self):
        args = log_details_parser.parse_args()
        tracker_id = args.get('Tracker-Id', None)    
        value = args.get("value", None)
        note = args.get("note")
        timestamp = args.get("timestamp", None)
        

        if value is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1002", error_message="password is required")

        if timestamp is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1005", error_message="email is required")

        try:
            new_log = Log(trakcer_id = tracker_id, value = value, note = note, timestamp = timestamp)
            db.session.add(new_log)
            db.session.commit()
            return "Log created successfully.", 201
        except:
            return "Unexpected error.", 500

    @auth_required('token')
    def get(self):
        args = log_details_parser.parse_args()
        tracker_id = args.get('Tracker-Id', None)  
        logs = db.session.query(Log).filter(Log.tracker_id == tracker_id).all()
        log_list = []
        for log in logs:
            log_list.append({'id': log.id, 'value' : log.value, 'note' : log.note, 'timestamp': log.timestamp})
        return log_list, 200

class Log2APPI(Resource):

    @auth_required('token')
    @marshal_with(log_details)
    def get(self, id):
        log = db.session.query(Log).filter(Log.id == id).first()
        return log, 200

    @auth_required('token')
    def patch(self, id):
        try:
            args = log_details_parser.parse_args()        
            value = args.get("value", None)
            note = args.get("note")
            timestamp = args.get("timestamp", None)

            log = db.session.query(Log).filter(Log.id == id).first()

            if value:
                log.value = value
            
            log.note = note

            if timestamp:
                log.timestamp = timestamp
                        
            db.session.commit()

            return "Update Successful", 200
        except:
            return "Unexpected error", 500

    @auth_required('token')
    def delete(self, id):
        try:
            log = db.session.query(Log).filter(Log.id == id).first()
            db.session.delete(log)
            db.session.commit()
            return "Deletion Successful", 200
        except:
            return "Unexpected error", 500       