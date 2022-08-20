from enum import unique
from .database import db


class User(db.Model):
    __tablename__ = 'User'

    userId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userName = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)


class Tracker(db.Model):
    __tablename__ = 'Tracker'

    trackerId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    type = db.Column(db.Integer, nullable=False)
    options = db.Column(db.String, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("User.userId"), nullable=False)


class Log(db.Model):
    __tablename__ = 'Log'

    logId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trackerId = db.Column(db.Integer, db.ForeignKey("Tracker.trackerId"),  nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.String, nullable=False)


class Options(db.Model):
    __tablename__ = 'Options'

    trackerId = db.Column(db.Integer, db.ForeignKey("Tracker.trackerId"), primary_key=True)
    name = db.Column(db.String, primary_key=True)


class TrackerType(db.Model):
    __tablename__ = 'TrackerType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


class Token(db.Model):
    __tablename__ = 'Token'

    token = db.Column(db.String, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("User.userId"), unique=True, nullable=False)
    expiry = db.Column(db.String, nullable=False)