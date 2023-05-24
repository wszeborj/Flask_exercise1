from . import db
from datetime import datetime


class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), unique=True)
    sign_in_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
