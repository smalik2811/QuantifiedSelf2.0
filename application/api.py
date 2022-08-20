from hmac import digest_size
from math import exp
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError, DuplicateResource
from application.models import User, Token
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort
import hashlib
from datetime import datetime, timedelta

# Parser used when creating new User
create_user_details = reqparse.RequestParser()
create_user_details.add_argument('userName')
create_user_details.add_argument('password')
create_user_details.add_argument('firstName')
create_user_details.add_argument('lastName')
create_user_details.add_argument('email')

# Parser used for user Logging
log_user_parser = reqparse.RequestParser()
log_user_parser.add_argument('userName')
log_user_parser.add_argument('password')

resource_fields = {
    'user_id':   fields.Integer,
    'userName':    fields.String,
    'email':    fields.String
}

token_response = {
    'token': fields.String
}


class UserAPI(Resource):

    def put(self):
        pass

    def post(self):
        args = create_user_details.parse_args()
        userName = args.get("userName", None)
        password = args.get("password", None)
        firstName = args.get("firstName", None)
        lastName = args.get("lastName", None)
        email = args.get("email", None)

        if userName is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1001", error_message="userName is required")

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

        user = db.session.query(User).filter(
            (User.userName == userName) | (User.email == email)).first()

        if user:
            raise BusinessValidationError(
                status_code=409, error_code="BE1007", error_message="userName already exist.")

        try:
            new_user = User(userName=userName, password=password,
                            firstName=firstName, lastName=lastName, email=email)
            db.session.add(new_user)
            db.session.commit()
            return "User created successfully.", 201
        except:
            return "Unexpected error.", 500

    def get(self):
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        token = bearer.split()[1] 
        return 200

    def delete(self):
        pass


class UserLoggingAPI(Resource):

    @marshal_with(token_response)
    def post(self):
        args = log_user_parser.parse_args()
        userName = args.get("userName", None)
        password = args.get("password", None)

        if userName is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1001", error_message="userName is required")

        if password is None:
            raise BusinessValidationError(
                status_code=400, error_code="BE1002", error_message="password is required")

        try:
            user = db.session.query(User).filter(
                User.userName == userName).first()
        except:
            return "Unexpected error.", 500

        if not user:
            return "Username not found.", 404

        if not user.password == password:
            return "Wrong password supplied.", 400

        try:
            # check if token already exist and delete if exist
            userId = user.userId
            old_token = db.session.query(Token).filter(Token.userId == userId).first()
            if old_token:
                db.session.delete(old_token)
                db.session.commit()
            expiry_date = datetime.now() + timedelta(1)
            user_name = str(userName) + expiry_date.strftime('%d%m%Y%H%M%S')
            formatted_expiry_date = expiry_date.strftime('%d-%m-%Y')
            token_value = hashlib.blake2b(user_name.encode(
                'utf-8'), digest_size=15).hexdigest()
            new_token = Token(token=token_value, userId=userId,
                              expiry=formatted_expiry_date)
            db.session.add(new_token)
            db.session.commit()
            return new_token

        except:
            return "Unexpected error.", 500
