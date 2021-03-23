from petstagram_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class Game(db.Model):
    """Game model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.Date)

    console_id = db.Column(
        db.Integer, db.ForeignKey('console.id'), nullable=False)
    console = db.relationship('Console', back_populates='games')

    collections = db.relationship(
        'Collection', secondary='game_collection', back_populates='games'
    )

    def __str__(self):
        return f'<Game: {self.title}>'

    def __repr__(self):
        return f'<Game: {self.title}>'


class Console(db.Model):
    """Console model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    games = db.relationship('Game', back_populates='console')

    def __str__(self):
        return f'<Console: {self.name}>'

    def __repr__(self):
        return f'<Console: {self.name}>'


class Collection(db.Model):
    """Collection model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    games = db.relationship(
        'Game', secondary='game_collection', back_populates='collections'
        )

    def __str__(self):
        return f'<Collection: {self.name}>'

    def __repr__(self):
        return f'<Collection: {self.name}>'


game_collection_table = db.Table(
    'game_collection',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'
