# database models stored here
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class ACdatum(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # main key that will be used to identify any saved ACdata instances
    hours = db.Column(db.Integer()) #how many hours they used theyre AC for
    temp = db.Column(db.Integer()) #the temperature they set their ac too
    sugg_hours = db.Column(db.Integer())
    sugg_temp = db.Column(db.Integer())
    estimated_bill = db.Column(db.Integer()) #estimated bill based on previous two factors
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # func.now() returns current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # connects ACdata to a user


class FanData(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)  # main key that will be used to identify any saved ACdata instances
    estimated_bill = db.Column(db.Integer()) #how much they spend daily
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # func.now() returns current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # connects ACdata to a user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary key is the main key for the user
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True)
    state = db.Column(db.String)
    priority = db.Column(db.String)
    budget = db.Column(db.Integer())
    BTU_rating = db.Column(db.Integer())
    wattage = db.Column(db.Integer())
    size = db.Column(db.String())
    typ = db.Column(db.String())
    EER = db.Column(db.Integer())
    ACdata = db.relationship('ACdatum')  # reference to ACdatum from User #ACdata is list of ACdatum
    fanData = db.relationship('FanData')
    totalMoneySaved = db.Column(db.Integer(), server_default="0")
