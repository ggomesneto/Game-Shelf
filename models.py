"""Models for database"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.Text, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    dob = db.Column(db.Date)
    email - db.Column(db.Text, nullable=False)

    favorites = db.relationship('Collection')
    reviews = db.relationship('Review')

    def __repr__(self):
        return f"<User {self.username} {self.first_name} {self.last_name}>"

class Collection(db.Model):

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, db.ForeignKey('User.username'))
    game_slug = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<favorite {self.username} {self.game_slug}"

class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, db.ForeignKey('User.username'))
    game_slug = db.Column(db.Text, nullable=False)
