import os
from unittest import result
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from application import workers
from application.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import User, Role

app = None
api = None
celery = None

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
      result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    return app, api, celery

app, api, celery = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

# Add all restful controllers
from application.api import *
api.add_resource(User1API, "/api/user")
api.add_resource(User2API, "/api/users")
api.add_resource(Tracker2API,"/api/tracker/<int:id>")
api.add_resource(Tracker1API, "/api/tracker")
api.add_resource(Log1API, "/api/log")
api.add_resource(Log2API, "/api/log/<int:id>")

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
