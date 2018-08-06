from project import db

from flask import request, redirect, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email          = db.Column(db.String, unique=True, nullable=False)
    password_hash  = db.Column(db.String, nullable=False)
    name           = db.Column(db.String, nullable=False)
    is_storyteller = db.Column(db.Boolean, nullable=False)
    birthday       = db.Column(db.String, nullable=True)
    country        = db.Column(db.String, nullable=True)
    profession     = db.Column(db.String, nullable=True)
    city           = db.Column(db.String, nullable=True)
    number         = db.Column(db.String, nullable=True)
    bio            = db.Column(db.String, nullable=True)
    about          = db.Column(db.String, nullable=True)
    profile_img    = db.Column(db.String, nullable=True)
    reason         = db.Column(db.String, nullable=True)

    def __init__(self, email,name,password, birthday='', country='', is_storyteller='',profession='', city='', number='', bio='', about=''):
        self.email       = email
        self.set_password(password)
        self.name           = name
        self.birthday       = birthday
        self.country        = country
        self.is_storyteller = is_storyteller
        self.profession     = profession
        self.city           = city
        self.number         = number
        self.bio            = bio
        self.about          = about

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User %d %s' % (self.id, self.email)

class Journey(UserMixin, db.Model):


    __tablename__ = "journey"


    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title        = db.Column(db.String, nullable=False)
    description  = db.Column(db.String, nullable=False)
    location     = db.Column(db.String, nullable=False)
    duration     = db.Column(db.String, nullable=False)
    category     = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    people_range = db.Column(db.String, nullable=False)
    price        = db.Column(db.String, nullable=False)
    picture      = db.Column(db.String, nullable=False)


    def __init__(self, creator_id='', title='', description='', location='', duration='', category='', requirements='', people_range='', picture='', price=''):
        self.creator_id    = creator_id
        self.title         = title
        self.description   = description
        self.location      = location
        self.duration      = duration
        self.category      = category
        self.requirements  = requirements
        self.people_range  = people_range
        self.picture       = picture
        self.price         = price


    def __repr__(self):
        return 'Journey %d %s' % (self.id, self.title)



class Ratings(UserMixin, db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    user = db.Column(db.String(30), nullable= False)
    stars = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(30), nullable= False)
    review = db.Column(db.String(30), nullable= False)
    time = db.Column(db.String(80), nullable = False)
    journey = db.relationship(Journey)

    def __init__(self, journey_id='', user='', stars='', title='', review=''):
        self.journey_id =journey_id
        self.user = user
        self.stars = stars
        self.title = title
        self.review = review
#############  I DIDN'T DO SELF TIME BUT IT WORKED SO I JUST LEFT IT  #####################

    def __repr__(self):
        return 'Ratings %r %s %r %s %r %s' % (self.id, self.title, self.journey_id, self.user, self.stars ,self.review)


class Notification(db.Model):
    __tablename__ = "notification"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interested_user_id = db.Column(db.Integer, db.ForeignKey('users.id') ,nullable=False)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)

    st = db.relationship("User", foreign_keys="Notification.st_id")
    user = db.relationship("User", foreign_keys="Notification.interested_user_id")
    journey = db.relationship("Journey", foreign_keys="Notification.journey_id")

    interested_user_name = db.Column(db.String(30), nullable= False)
    journey_title = db.Column(db.String(30), nullable= False)
    time = db.Column(db.String(80), nullable = False)


    def __init__(self, st_id='', journey_id='', interested_user_id='', interested_user_name='', journey_title='', time=''):
        self.st_id = st_id
        self.journey_id = journey_id
        self.interested_user_id = interested_user_id
        self.interested_user_name = interested_user_name
        self.journey_title = journey_title
        self.time = time

    def __repr__(self):
        return 'Notification %r %r %r %r' % (self.id, self.st_id, self.journey_id, self.interested_user_id)


class Wishlist(db.Model):
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    journey_title = db.Column(db.String(30), nullable= False)

    def __init__(self, user_id='', journey_id='', journey_title=''):
        self.user_id = user_id
        self.journey_id = journey_id
        self.journey_title = journey_title

    def __repr__(self):
        return 'Wishlist %r %r' % (self.id, self.user_id, self.journey_id)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journey_id = db.Column(db.Integer, db.ForeignKey('journey.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(30), nullable = False)
    question = db.Column(db.String(80), nullable = False)
    time = db.Column(db.String(80), nullable = False)
    # reply = db.relationship('Reply', backref='question')
    
    def __init__(self, journey_id='',user_id='', title='', question='', time=''):
        self.journey_id = user_id
        self.user_id = user_id
        self.title = title
        self.question = question
        self.time = time


    def __repr__(self):
        return '<Question %r>' % self.title




# db.drop_all()
# db.create_all()

