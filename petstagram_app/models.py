from petstagram_app import db
from sqlalchemy.orm import backref
from sqlalchemy_utils import URLType
from flask_login import UserMixin


class Post(db.Model):
    """Post model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(280), nullable=False)
    user = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(URLType)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'
