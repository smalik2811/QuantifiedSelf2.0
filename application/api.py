from hmac import digest_size
from math import exp
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError, DuplicateResource
from application.models import User
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort
from flask_security import auth_required
from flask_login import current_user

# Parser used when creating new User
create_user_details = reqparse.RequestParser()
create_user_details.add_argument('username')
create_user_details.add_argument('password')
create_user_details.add_argument('firstName')
create_user_details.add_argument('lastName')
create_user_details.add_argument('email')

# Parser used for user Logging
log_user_parser = reqparse.RequestParser()
log_user_parser.add_argument('userName')
log_user_parser.add_argument('password')

personal_details = {
    'username':    fields.String,
    'first_name' : fields.String,
    'last_name' : fields.String,
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
        userName = args.get("username", None)
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
            (User.username == userName) | (User.email == email)).first()

        if user:
            raise BusinessValidationError(
                status_code=409, error_code="BE1007", error_message="userName already exist.")

        try:
            new_user = User(username=userName, fs_uniquifier=userName, password=password,
                            first_name=firstName, last_name=lastName, email=email, active=1, role=1)
            db.session.add(new_user)
            db.session.commit()
            return "User created successfully.", 201
        except:
            return "Unexpected error.", 500

    # @marshal_with(personal_details)
    @auth_required("token")
    def get(self):
        print("hello world")
        a = current_user
        return current_user.username

    def delete(self):
        pass

