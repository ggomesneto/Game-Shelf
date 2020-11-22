from app import app
from models import db, Review, User, Collection

db.drop_all()
db.create_all()

user1 = User(
    username='ggomesneto',
    first_name='Geraldo',
    last_name='Gomes',
    email='email@email.com'
    
)

collection1 = Collection(
    username='ggomesneto',
    game_slug='the-witcher-3-wild-hunt'
)

review1 = Review(
    username='ggomesneto',
    game_name='The Witcher 3 Wild Hunt',
    game_slug='the-witcher-3-wild-hunt',
    review='AWESOME GAME',
    title='I LOVE THIS GAME'
)

db.session.add_all([user1,collection1,review1])
db.session.commit()