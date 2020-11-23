from flask import Flask, request, render_template, redirect, Markup, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
from sqlalchemy import desc, exc


from models import db, connect_db, User, Collection, Review
from forms import RegisterForm, LoginForm


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

    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect('/login')
    
    else:
        resp = requests.get(f"https://rawg.io/api/games/{id}")
        data = resp.json()
        status = resp.status_code

        # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE
        if status == 200:

            name = data['name']
            title = "Add Review"
            game_slug = id
            username = session['username']
            function = Markup('<script> addReview() </script>')

            return render_template('review_form.html', game_slug=game_slug, title=title,function=function, name=name, username=username)


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

@app.route('/reviews')
def reviews_route():
    '''SHOW LIST OF LAST ADDED REVIEWS, FROM ALL THE GAMES'''
    title='Last added reviews'

    reviews = Review.query.all()

    function= Markup('<script> getReviews();</script>')

    return render_template('reviews.html',title=title, function=function, reviews=reviews)


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


@app.route('/<id>/collection')
def collection_page(id):

    user = User.query.filter_by(username=id).first()

    if user:
        title=f"{user.username} Collection:"
        function = Markup(f"<script> getPlatInfo(); getCollection('{id}')</script>")
        return render_template('index.html', title=title, function=function)
    else:
        return redirect('/')


# ----------------LOGIN / LOGOUT / REGISTER ---------------
@app.route('/login', methods=['GET','POST'])
def login_route():

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name,pwd)

        if user:
            session['username'] = user.username
            return redirect('/')
        else:
            form.username.errors = ['Bad name/password']


    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    '''Register user: produce form & handle form submission'''

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, first_name, last_name)

        try:
            db.session.add(user)
            db.session.commit()

            session['username'] = user.username

            # on a successfull login, redirect to main page
            return redirect('/')

        except exc.IntegrityError:
            db.session.rollback()
            flash(f"{name} already exists")
            return redirect('/register')

    else:
        return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


# ----------------- ROUTES TO REQUEST DATA FROM DATABASE ---------------------
@app.route('/api/reviews')
def get_reviews():

    reviews = [review.serialize() for review in Review.query.order_by(desc(Review.id)).limit(10).all()]
    
    return jsonify(reviews=reviews)
    
@app.route('/api/<id>/collection')
def get_collection(id):

    user = User.query.filter_by(username=id).first()
    collection = [ favorite.serialize() for favorite in user.favorites] 

    return jsonify(collection=collection)

@app.route('/api/review/<id>', methods=['DELETE'])
def delete_review(id):

    review = Review.query.get(id)

    db.session.delete(review)
    db.session.commit()
    
    return jsonify(message='Deleted')

    
@app.route('/islogged')
def is_logged():

    if 'username' in session:
        username = session['username']
        favorites = [favorite.serialize()['game_slug'] for favorite in Collection.query.filter_by(username=username)]

        return jsonify(islogged=True, username=username, game_slug=favorites)

    else:
        return jsonify(islogged=False)

@app.route('/api/favorite', methods=['POST'])
def add_favorite():

    if 'username' in session:
        username = session['username']
        slug = request.json['slug']

        favorite = Collection(username=username, game_slug=slug)

        db.session.add(favorite)
        db.session.commit()
        response_json = jsonify(favorite=favorite.serialize())
        return (response_json, 201)
    else:
        flash('You must be logged in to view')
        return redirect('/login')
        

@app.route('/api/favorite/<slug>', methods=['DELETE'])
def delete_favorite(slug):

    if 'username' in session:
        username = session['username']
        slug = slug

        favorite = Collection.query.filter_by(username=username).filter_by(game_slug=slug).first()

        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify(message='Deleted')
    else:
        flash('You must be logged in to view')
        return redirect('/login')