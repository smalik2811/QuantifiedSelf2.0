from hmac import digest_size
from math import exp
from urllib import request
from flask_restful import Resource, Api, request
from flask_restful import fields, marshal_with, marshal
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError, DuplicateResource
from application.models import User
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort
from flask_security import auth_required
from flask_login import current_user

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

