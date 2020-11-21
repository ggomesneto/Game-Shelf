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

    favorites = db.relationship('Favorite')

    def __repr__(self):
        return f"<User {self.username} {self.first_name} {self.last_name}>"

class Favorite(db.Model):

    __tablename__ = 'favorites'

    username = db.Column(db.Text, db.ForeignKey('User.username'), primary_key=True)
    game_slug = db.Column(db.Text, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<favorite {self.username} {self.game_slug}"