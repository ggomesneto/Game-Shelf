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
    email = db.Column(db.Text, nullable=False)

    favorites = db.relationship('Collection')
    reviews = db.relationship('Review')

    def __repr__(self):
        return f"<User {self.username} {self.first_name} {self.last_name}>"

    def serialize(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }


class Collection(db.Model):

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, db.ForeignKey('users.username'))
    game_slug = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<favorite {self.username} {self.game_slug}"

    def serialize(self):
        return {
            'username': self.username,
            'game_slug': self.game_slug
        }

class Review(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, db.ForeignKey('users.username'))
    game_name = db.Column(db.Text, nullable=False)
    game_slug = db.Column(db.Text, nullable=False)
    review = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'username': self.username,
            'game_name': self.game_name,
            'game_slug': self.game_slug,
            'review': self.review,
            'title': self.title
        }
