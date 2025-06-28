from flask import Blueprint
from . import db
from flask_login import current_user, UserMixin

class Users(db.Model, UserMixin):
    #simple user model with email, password, id, optional username and an equiries feild
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    inquiries = db.relationship('Inquiries', backref='user', lazy=True)
    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    @classmethod
    def make_user(cls, email, password, username):
        new_user = cls(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
class Inquiries(db.Model):
    #simple inquiry model with id, user_id, and a message
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(500))
    @classmethod
    def make_inquiry(cls, user_id, message):
        new_inquiry = cls(user_id=user_id, message=message)
        db.session.add(new_inquiry)
        db.session.commit()
        return new_inquiry