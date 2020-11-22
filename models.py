"""Models for database"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'


    username = db.Column(db.Text, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)


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

    @classmethod
    def register(cls, username, pwd, first_name, last_name):
        '''Register user with hashed password & return user'''

        hashed = bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')

        #return instance of user with username and hashed pwd
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        '''Validate that user exists & password is correct.

        Return user if valid; else return false'''

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False



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
