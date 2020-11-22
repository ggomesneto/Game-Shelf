from flask import Flask, request, render_template, redirect, Markup, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
from sqlalchemy import desc 

from models import db, connect_db, User, Collection, Review


app = Flask(__name__)

'''BOILER PLATE FOR SQLALCHEMY, DEBUGTOOLBAR AND FLASK'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///gameshelf'
app.config['SECRET_KEY'] = 'abc'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def default_page():
    '''DEFAULT PAGE WITH FUNCTION TO SEARCH FOR TRENDING GAMES'''
    title = 'New and Trending'
    function = Markup('<script>  getPlatInfo(); startSearch();</script>')
    return render_template('index.html', title=title, function=function)


@app.route('/games/<id>')
def games_route(id):
    '''ROUTE TO PAGE WITH MORE DEEP INFORMATION ABOUT A GAME'''
    resp = requests.get(f"https://rawg.io/api/games/{id}")
    data = resp.json()
    status = resp.status_code



    # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE
    if status == 200:

        reviews = Review.query.filter_by(game_slug=id).order_by(desc(Review.id)).limit(10).all()

        slug = id
        title = data['name']
        platforms = data['platforms']
        description = Markup(data['description'])
        genres = data['genres']
        developers = data['developers']
        esrb_rating = data['esrb_rating']
        metacritic = data['metacritic']
        publishers = data['publishers']
        released = data['released']
        website = data['website']
        stores = data['stores']
        images = [ data['background_image'], data['background_image_additional']]


        return render_template('game_info.html', slug=slug, title=title, platforms=platforms, description=description, genres=genres, developers=developers, esrb_rating=esrb_rating, metacritic=metacritic, publishers=publishers, released=released, website=website, images=images, stores=stores, reviews=reviews)
    else:
        return redirect('/')

@app.route('/games/<id>/review')
def review_form(id):

    resp = requests.get(f"https://rawg.io/api/games/{id}")
    data = resp.json()
    status = resp.status_code

    # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE
    if status == 200:

        name = data['name']
        title = "Add Review"
        game_slug = id
        function = Markup('<script> addReview() </script>')

        return render_template('review_form.html', game_slug=game_slug, title=title, function=function, name=name)

    
    else:
        return redirect('/')


@app.route('/games/<id>/review', methods=['POST'])
def add_review(id):

    db.session.rollback()
    resp = requests.get(f"https://rawg.io/api/games/{id}")
    data = resp.json()
    status = resp.status_code

    # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE
    if status == 200:
       
        game_slug = id
        username = request.form['username']
        game_name = request.form['game_name']
        review = request.form['review']
        title = request.form['title']

        review = Review(username=username, game_name=game_name, game_slug=game_slug, review=review, title=title)

        db.session.add(review)
        db.session.commit()

        return redirect(f"/games/{id}")

        



@app.route('/genres/<id>')
def genres_route(id):
    '''ROUTE TO SEARCH BY GENRE'''

    resp = requests.get(f"https://api.rawg.io/api/games?genres={id}")
    status = resp.status_code
    data = resp.json()

    # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE
    if len(data['results']) > 0:
        title = id.upper()
        function = Markup('<script>getGenre()</script>')
        return render_template('index.html', title=title, function=function)
    else:
        return redirect('/')

@app.route('/platforms/<id>')
def plat_route(id):
    '''ROUTE FOR PLATFORMS'''
    
    platforms = requests.get('https://api.rawg.io/api/platforms').json()
    
    for platform in platforms['results']:
        
        if platform['id'] == int(id):
            title = platform['name']
            resp = requests.get(f"https://api.rawg.io/api/games?platforms={id}")

            status = resp.status_code
            data = resp.json()
            function = Markup('<script>getPlatform()</script>')
            return render_template('index.html', title=title, function=function)
    
    return redirect('/')
        
@app.route('/search')
def search_route():
    ''' ROUTE FOR THE MAIN SEARCH AREA'''
    title = request.args['search'].upper()

    function = Markup('<script>searchBox()</script>')

    return render_template('index.html', title=title, function=function)

@app.route('/reviews')
def reviews_route():
    '''SHOW LIST OF LAST ADDED REVIEWS, FROM ALL THE GAMES'''
    title='Last added reviews'
    function= Markup('<script> getReviews();</script>')

    return render_template('index.html',title=title, function=function)




# ----------------- ROUTES TO REQUEST DATA FROM DATABASE ---------------------
@app.route('/api/reviews')
def get_reviews():

    reviews = [review.serialize() for review in Review.query.order_by(desc(Review.id)).limit(10).all()]
    print(reviews)
    return jsonify(reviews=reviews)
    

# ADD TO DATABASE A QUERY THAT SHOWS USERS WITH THE SAME GAMES.MAYBE A PERSONAL CHAT OR SOMETHING


@app.route('/login')
def login_route():

    return render_template('login.html')