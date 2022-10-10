from mypass import db, loginManager
from datetime import datetime
from flask_login import UserMixin


@loginManager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(db.Model):
    id = db.Column('id_user', db.Integer, primary_key=True)
    last_name = db.Column('last_name', db.String(length=100), nullable=False)
    first_name = db.Column('first_name', db.String(length=100), nullable=False)
    image_profile = db.Column(db.String(200), nullable=False,
                              default='./thumbnail/default.png')
    email = db.Column('user_email', db.String(
        length=100), unique=True, nullable=False)
    password = db.Column('password', db.String(length=100), nullable=False)
    user_id = db.Column('user_id', db.String(
        length=100), unique=True, nullable=False)
    date_signup = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)


class Type_Event(db.Model):
    id = db.Column('id_type', db.Integer, primary_key=True)
    name = db.Column('event_name', db.String(length=100), nullable=False)


class Category(db.Model):
    id = db.Column('id_category', db.Integer, primary_key=True)
    category = db.Column('category_name', db.String(
        length=100), nullable=False)


class Events(db.Model):
    id = db.Column('id_events', db.Integer, primary_key=True)
    title = db.Column('event_title', db.String(length=100), nullable=False)
    category = db.Column('category', db.Integer,
                         db.ForeignKey(Category.id), nullable=False)
    author = db.Column('author', db.Integer,
                       db.ForeignKey(Users.id), nullable=False)
    type = db.Column(db.Integer, db.ForeignKey(Type_Event.id), nullable=False)
    place = db.Column('event_place', db.String(length=100), nullable=False)
    date_event = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    time_event = db.Column(db.Time, nullable=False)
    seat = db.Column('nombre_places', db.Integer, nullable=False)
    image = db.Column('image', db.String(length=200),
                      default='defaultTheme.png')
    date_post = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)


class Tickets(db.Model):
    id = db.Column('id_participant', db.Integer, primary_key=True)
    user = db.Column('user_name', db.Integer,
                     db.ForeignKey(Users.id), nullable=False)
    event = db.Column('event_name', db.Integer,
                      db.ForeignKey(Events.id), nullable=False)
    nombre_ticket = db.Column('ticket', db.Integer, nullable=False)
