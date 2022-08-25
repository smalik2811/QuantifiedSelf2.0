from hmac import digest_size
from math import exp
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
import json

# Parser for User
user_details = reqparse.RequestParser()
user_details.add_argument('email')
user_details.add_argument('password')
user_details.add_argument('firstName')
user_details.add_argument('lastName')


personal_details = {
    'first_name' : fields.String,
    'last_name' : fields.String,
    'email':    fields.String
}



# Parser for Tracker
tracker_details = reqparse.RequestParser()
tracker_details.add_argument('name')
tracker_details.add_argument('description')
tracker_details.add_argument('type', type=int)
tracker_details.add_argument('options', action='append')


class UserAPI(Resource):

    def post(self):
        args = user_details.parse_args()        
        email = args.get("email", None)
        password = args.get("password", None)
        firstName = args.get("firstName", None)
        lastName = args.get("lastName", None)

        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1002", error_message="password is required")

        if firstName is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1003", error_message="firstName is required")

        if email is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1005", error_message="email is required")

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
    @marshal_with(personal_details)
    def get(self):
        try:
            return current_user, 200
        except:
            return "Unexpected error", 500
    
    @auth_required("token")
    def patch(self):
        try:
            args = user_details.parse_args()        
            email = args.get("email", None)
            password = args.get("password", None)
            firstName = args.get("firstName", None)
            lastName = args.get("lastName", None)

            logged_user = db.session.query(User).filter(User.email == current_user.email).first()

            if email:
                logged_user.email = email
            
            if password:
                logged_user.password = password
            
            if firstName:
                logged_user.first_name = firstName

            if lastName:
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
            args = tracker_details.parse_args()
            name = args.get('name', None)
            description = args.get('description', None)
            type = args.get('type', None)
            options = args.get('options', None)

            if name is None:
                raise BusinessValidationError(400, "BE008", "Tracker name is required")
            
            if type is None:
                raise BusinessValidationError(400, "BE009", "Tracker type is required.")
            
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
        return json.dumps(trackers), 200


class Tracker2API(Resource):
    
    @auth_required('token')
    def get(self, name):
        tracker = db.session.query(Tracker).filter(Tracker.name == name).first()
        return json.dumps(tracker), 200