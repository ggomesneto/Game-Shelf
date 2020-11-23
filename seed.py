from app import app
from models import db, Review, User, Collection

db.drop_all()
db.create_all()

name='JohnLennon',
pwd='123'
first_name='John',
last_name='Lennon',

user1 = User.register(name,pwd,first_name, last_name)

name='RingoStar',
pwd='123'
first_name='Ringo',
last_name='Star',

user2 = User.register(name,pwd,first_name, last_name)

collection1 = Collection(
    username='JohnLennon',
    game_slug='the-witcher-3-wild-hunt'
)

collection2 = Collection(
    username='RingoStar',
    game_slug='fall-guys'
)

review1 = Review(
    username='JohnLennon',
    game_name='The Witcher 3 Wild Hunt',
    game_slug='the-witcher-3-wild-hunt',
    review='AWESOME GAME',
    title='I LOVE THIS GAME'
)

review2 = Review(
    username='RingoStar',
    game_name='Cyberpunk 2077',
    game_slug='cyberpunk-2077',
    review='Wow',
    title='Nyce'
)

db.session.add_all([user1, user2,collection1, collection2,review1,review2])
db.session.commit()