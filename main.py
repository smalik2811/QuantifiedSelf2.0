import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required, hash_password
from application.models import User, Role

app = None
api = None


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
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import home

# Add all restful controllers
from application.api import *
api.add_resource(UserAPI, "/user")
api.add_resource(Tracker2API,"/tracker/<string:name>")
api.add_resource(Tracker1API, "/tracker")
api.add_resource(Log1API, "/log")
api.add_resource(Log2APPI, "/log/<int:id>")

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
