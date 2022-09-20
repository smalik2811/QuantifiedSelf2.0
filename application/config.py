import os
from smtplib import SMTP
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG = True
    SECRET_KEY = "34e34f1486aa88e0b0335d70b3e228" # Some strong random key.
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "34e34f14" # Seed
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = False
    SECURITY_LOGIN_URL = "/api/user/login"
    SECURITY_LOGOUT_URL = "/api/user/logout"
    SECURITY_BACKWARDS_COMPAT_UNAUTHN = True
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAwvcHlMM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=vn85jvSd-pdPlUMgYhmgb3aemG8BPbmoEDFXby2rVoE%3D"
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "quantified.notifier@quant.com"
    SENDER_PASSWORD = ""