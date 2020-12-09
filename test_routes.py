
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, connect_db, User, Collection, Review

# FLASK_ENV=production python -m unittest test_routes.py


os.environ['DATABASE_URL'] = "postgresql:///gameshelftest"



from app import app


db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCasse(TestCase):
    """Test views for messages."""

    def setUp(self):

        Review.query.delete()
        Collection.query.delete()
        User.query.delete()

        self.client = app.test_client()

        db.session.commit()

    def test_user_model(self):
        '''Testing user model'''

        u = User.register(username='JohnS',pwd='abc123',first_name='John',last_name='Smith')

        db.session.add(u)
        db.session.commit()
        
        users = User.query.all()

        self.assertEqual(len(users), 1)

        try:
            db.session.add(u)
            db.session.commit()
        except exc.IntegrityError:
            self.assertRaises(exc.IntegrityError)

    def test_authenticate(self):

        u = User.register(username='JohnS',pwd='abc123',first_name='John',last_name='Smith')

        db.session.add(u)
        db.session.commit()

        username = 'JohnS'
        password = 'abc1234'

        user = User.authenticate(username, password)

        self.assertFalse(user)

    def test_collection(self):

        u = User.register(username='JohnS',pwd='abc123',first_name='John',  last_name='Smith')

        db.session.add(u)
        db.session.commit()


        c = Collection(username='JohnS', game_slug='fall-guys')

        db.session.add(c)
        db.session.commit()

        collections = Collection.query.all()

        self.assertEqual(len(collections), 1)

    def test_review(self):

        u = User.register(username='JohnS',pwd='abc123',first_name='John',  last_name='Smith')

        db.session.add(u)
        db.session.commit()

        r = Review(username='JohnS',game_name='Fall Guys',game_slug='fall-guys',review='good game', title='i love it')

        db.session.add(r)
        db.session.commit()

        reviews = Review.query.all()

        self.assertEqual(len(reviews),1)




        