from .database import db
from flask_security import UserMixin, RoleMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    fs_uniquifier = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean())
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)


class Tracker(db.Model):
    __tablename__ = 'tracker'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    type = db.Column(db.Integer, db.ForeignKey("tracker_type.id") ,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)


class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey("Tracker.id"),  nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.String, nullable=False)


class Options(db.Model):
    __tablename__ = 'options'

    tracker_id = db.Column(db.Integer, db.ForeignKey("Tracker.id"), primary_key=True)
    name = db.Column(db.String, primary_key=True)


class TrackerType(db.Model):
    __tablename__ = 'tracker_type'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
