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

    # IM ADDING A SCRIPT ON THE HTML FILE, SO IT WILL ACTIVATE THE FUNCTIONS I NEED FROM TH APP.JS FILE
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

        # GET A MAX OF 10 REVIEWS, FROM THE NEWEST TO THE OLDEST AND ADD TO THE GAMES INFO PAGE
        reviews = Review.query.filter_by(game_slug=id).order_by(desc(Review.id)).limit(10).all()

        # I DECIDED TO MAKE THE API REQUEST HERE, SO THE NEXT LINES ARE BASICALLY TO GET THE INFORMATION I WANT TO BE SHOWN ON THE HTML
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
        # IF THE STATUS IS NOT 200, THE USER IS REDIRECTED TO THE MAIN PAGE
        return redirect('/')

@app.route('/games/<id>/review')
def review_form(id):
    '''ROUTE TO ADD A REVIEW ABOUT A GAME. USER NEEDS TO BE LOGGED IN TO ACCESS THIS PAGE'''

    if 'username' not in session:
        # CHECK IF THE USER IS LOGGED IN. IF NOT, REDIRECT TO THE LOGIN PAGE
        flash('You must be logged in to view')
        return redirect('/login')
    
    else:
        # IF THE USER IS LOGGED IN, REQUEST THE DATA FROM THE GAME
        # THE ID ON THE URL IS THE GAME-SLUG. I NEED TO REQUEST INFO ABOUT THE GAME TO GET THE GAME NAME SO I CAN GET THE GAME NAME

        resp = requests.get(f"https://rawg.io/api/games/{id}")
        data = resp.json()
        status = resp.status_code

        # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE
        if status == 200:
            
            name = data['name']
            title = "Add Review"
            game_slug = id
            username = session['username']

            # IM ADDING A SCRIPT ON THE HTML FILE, SO IT WILL ACTIVATE THE FUNCTIONS I NEED FROM TH APP.JS FILE
            function = Markup('<script> addReview() </script>')

            # THIS TEMPLATE SHOWS A FORM WITH DATA THAT CAN'T BE MODIFIED, SUCH AS USERNAME AND GAME NAME. WHEN SUBMITTED, IT ADDS THE REVIEW TO THE DATABASE
            return render_template('review_form.html', game_slug=game_slug, title=title,function=function, name=name, username=username)

        else:
            return redirect('/')

@app.route('/games/<id>/review', methods=['POST'])
def add_review(id):
    '''POST ROUTE TO ADD A REVIEW TO THE DATABASE'''

    if 'username' not in session:
        # CHECK IF THE USER IS LOGGED IN. IF NOT, REDIRECT TO THE LOGIN PAGE
        flash('You must be logged in to view')
        return redirect('/login')
    
    else:
        # ROLLBACK JUST TO MAKE SURE THE SESSION IS EMPTY
        db.session.rollback()

        # REQUESTING DATA ABOUT THE GAME, JUST TO MAKE SURE THE GAME EXISTS
        resp = requests.get(f"https://rawg.io/api/games/{id}")
        data = resp.json()
        status = resp.status_code

        # IF THE STATUS IS GOOD, GET THE DATA FROM THE FORM AND ADD IT TO THE REVIEW TABLE ON THE DATABASE
        if status == 200:
        
            game_slug = id
            username = request.form['username']
            game_name = request.form['game_name']
            review = request.form['review']
            title = request.form['title']

            review = Review(username=username, game_name=game_name, game_slug=game_slug, review=review, title=title)

            db.session.add(review)
            db.session.commit()

            # REDIRECT TO THE GAME PAGE
            return redirect(f"/games/{id}")

@app.route('/reviews')
def reviews_route():
    '''SHOW LIST OF LAST ADDED REVIEWS, FROM ALL THE GAMES'''
    title='Last added reviews'

    # GETS ALL THE REVIEWS AND SHOW THEM ON THE PAGE
    reviews = Review.query.all()

    # IM ADDING A SCRIPT ON THE HTML FILE, SO IT WILL ACTIVATE THE FUNCTIONS I NEED FROM TH APP.JS FILE
    function= Markup('<script> getReviews();</script>')

    # RENDER SPECIFIC TEMPLATE WITH ALL REVIEWS ON THE DATABASE
    return render_template('reviews.html',title=title, function=function, reviews=reviews)

@app.route('/genres/<id>')
def genres_route(id):
    '''ROUTE TO SEARCH BY GENRE'''

    # GETS DATA BASED ON SPECIFIC GAME
    resp = requests.get(f"https://api.rawg.io/api/games?genres={id}")
    status = resp.status_code
    data = resp.json()

    # CHECK TO SEE IF THERE ARE RESULTS. IF NOT, REDIRECT TO MAIN PAGE. THIS IS USED TO CHECK IF THE URL IS WRITTEN CORRECTLY.
    # IN THIS CASE, I DECIDED TO USE AJAX AND JS TO ADD THE GAMES TO THE HTML PAGE.

    if len(data['results']) > 0:

        title = id.upper()

        # IM ADDING A SCRIPT ON THE HTML FILE, SO IT WILL ACTIVATE THE FUNCTIONS I NEED FROM TH APP.JS FILE
        function = Markup('<script>getGenre()</script>')

        return render_template('index.html', title=title, function=function)
    else:
        # IF THERE IS NO RESULTS, THE GENRE IS NOT PART OF THE API OR IS WRITTEN WRONG. IT REDIRECTS TO THE MAIN PAGE
        return redirect('/')

@app.route('/platforms/<id>')
def plat_route(id):
    '''ROUTE FOR PLATFORMS'''
    
    # THIS IS THE TRICKY PART OF THE API. TO MAKE IT WORK I HAD TO GET A LIST OF ALL THE PLATFORMS
    # MAKE A FOR LOOP COMPARING IT WITH THE ID. IF IT FINDS A MATCH, IT RETURNS A PAGE WITH A FUNCTION
    # THAT USES AJAX TO GET THE GAMES AND APPEND THEM TO THE HTML PAGE
    platforms = requests.get('https://api.rawg.io/api/platforms').json()
    
    for platform in platforms['results']:
        
        if platform['id'] == int(id):
            title = platform['name']

            # resp = requests.get(f"https://api.rawg.io/api/games?platforms={id}")

            # status = resp.status_code
            # data = resp.json()
            function = Markup('<script>getPlatform()</script>')
            return render_template('index.html', title=title, function=function)
    
    # IF THERE IS NO MATCH WITH THE PLATFORM NAME, REDIRECTS TO THE MAIN PAGE
    return redirect('/')
        
@app.route('/search')
def search_route():
    ''' ROUTE FOR THE MAIN SEARCH AREA'''
    title = request.args['search'].upper()

    # THE SEARCH IS MADE WITH AJAX. I'M ADDING THE FUNCTION TO THE PAGE SO IT WILL ACTIVATE IT.
    # THE USER DOESNT NEED TO BE LOGGED IN TO MAKE A SEARCH.

    function = Markup('<script>searchBox()</script>')

    return render_template('index.html', title=title, function=function)


@app.route('/<id>/collection')
def collection_page(id):
    '''ROUTE FOR THE COLLECTION PAGE'''

    # ANOTHER TRICKY PART. THE JS FUNCTION MAKES A REQUEST TO THE DATABASE TO GET A LIST OF FAVORITED GAMES
    # FROM THE USER SPECIFIED ON THE URL ID. IF THE USER LOGGED IN IS THE SAME AS THE URL ID, THERE WILL BE
    # A BUTTON ON THE GAMES TO REMOVE THE GAMES FROM THE COLLECTION. IF THE LOGGED IN USER IS ONLY CHECKING
    # ANOTHER USER'S COLLECTION, THE BUTTON WON'T APPEAR.
    
    user = User.query.filter_by(username=id).first()


    if user:

        if 'username' in session:
            user_logged = session['username']
            title=f"{user.username} Collection:"


            # THE getPlatInfo FUNCTION IS EXPLAINED IN DEPTH ON THE JS FILE

            # SINCE THE REQUEST AND THE APPEND IS MADE WITH JS, I HAVE TO CREATE A FUNCTION THAT REQUIRES BOTH THE
            # USERNAME OF LOGGED IN USER AND THE USERNAME OF THE COLLECTION'S OWNER TO COMPARE THEN.

            function = Markup(f"<script> getPlatInfo(); getCollection('{id}','{user_logged}')</script>")
            return render_template('index.html', title=title, function=function)
        else:
            user_logged = ''
            title=f"{user.username} Collection:"


            # THE getPlatInfo FUNCTION IS EXPLAINED IN DEPTH ON THE JS FILE

            # SINCE THE REQUEST AND THE APPEND IS MADE WITH JS, I HAVE TO CREATE A FUNCTION THAT REQUIRES BOTH THE
            # USERNAME OF LOGGED IN USER AND THE USERNAME OF THE COLLECTION'S OWNER TO COMPARE THEN.

            function = Markup(f"<script> getPlatInfo(); getCollection('{id}','{user_logged}')</script>")
            return render_template('index.html', title=title, function=function)

    else:
        # IF THERE IS NO USER WITH THE ID SPECIFIED ON THE URL, REDIRECT IT TO THE MAIN PAGE
        return redirect('/')


# ----------------LOGIN / LOGOUT / REGISTER ---------------
@app.route('/login', methods=['GET','POST'])
def login_route():
    '''ROUTE FOR THE LOGIN'''

    # WTFORMS. CHECK VALIDATION, AND IF THE USERNAME AND PASSWORD MATCHES WITH AN USER ON THE DATABASE
    # ADDS THE USERNAME TO THE SESSION, SO THE USER WILL STAY CONNECTED.
    # IF IT DOESNT MATCH, RETURNS AN ERROR

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
    '''ROUTE FOR REGISTRATION. TRY/EXCEPT FOR UNIQUE USERNAME'''

    # WTFORMS. VALIDATE FORM AND ADD THE INFO TO THE DATABASE
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, first_name, last_name)

        # TRIES TO ADD THE USER TO THE DATABASE. IF THE USERNAME ALREADY EXISTS IT ROLLBACK THE SESSION, FLASHES AN ERROR AND REDIRECT TO THE FORM PAGE.
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
    '''ROUTE TO LOGOUT'''

    # SIMPLY POP THE SESSION['USERNAME']
    session.pop('username')
    return redirect('/')


# ----------------- ROUTES TO REQUEST DATA FROM DATABASE ---------------------

@app.route('/api/reviews')
def get_reviews():
    '''ROUTE TO GET REVIEWS FROM THE DATABASE'''

    # GETS AN ARRAY OF SERIALIZE REVIEWS FROM THE DATABASE AND JSONIFY THEM.
    reviews = [review.serialize() for review in Review.query.order_by(desc(Review.id)).limit(10).all()]
    
    return jsonify(reviews=reviews)
    
@app.route('/api/<id>/collection')
def get_collection(id):
    '''ROUTE TO GET THE COLLECTION OF AN USER'''

    # SEARCH THE USER AND USE THE 'FAVORITE' RELATIONSHIP TO GET THE LIST OF THE COLLECTION GAMES.
    # CREATES AN SERIALIZED ARRAY WITH THE GAMES AND JSONIFY THEM.
    user = User.query.filter_by(username=id).first()
    collection = [ favorite.serialize() for favorite in user.favorites] 

    return jsonify(collection=collection)

@app.route('/api/review/<id>', methods=['DELETE'])
def delete_review(id):
    '''ROUTE TO DELETE A REVIEW'''

    # SELECT THE REVIEW BY ITS ID AND DELETE THEM.
    review = Review.query.get_or_404(id)

    db.session.delete(review)
    db.session.commit()
    
    return jsonify(message='Deleted')

@app.route('/islogged')
def is_logged():
    '''ROUTE TO CHECK IF USER IS LOGGED IN'''

    # THIS IS A ROUTE TO CHECK IF USER IS LOGGED IN SO THE JS FUNCTIONS CAN APPEND THE CORRECT HTML TO THE PAGE
    # LIKE, FOR EXAMPLE, IN THE MAIN PAGE, FOR EACH GAME THE 'FAVORITED BUTTON' HAS TO SHOW ADD OR REMOVE DEPENDING
    # ON THE LOGGED IN INFO.
    if 'username' in session:
        username = session['username']
        favorites = [favorite.serialize()['game_slug'] for favorite in Collection.query.filter_by(username=username)]
        
        # RETURNS INFORMATION ABOUT THE LOGGED IN USER TO APPEND THE CORRECT BUTTONS TO THE HTML.
        return jsonify(islogged= 'username' in session, username=username, game_slug=favorites)
    else:
        return jsonify(islogged= 'username' in session)
    
@app.route('/api/favorite', methods=['POST'])
def add_favorite():
    '''ROUTE TO ADD A FAVORITE'''

    # CHECK IF USER IS LOGGED IN. IF NOT, REDIRECTS TO LOGIN PAGE
    if 'username' in session:
        username = session['username']
        slug = request.json['slug']

        # GETS INFO FROM THE AJAX POST REQUEST AND ADD IT TO THE DATABASE
        favorite = Collection(username=username, game_slug=slug)

        db.session.add(favorite)
        db.session.commit()
        response_json = jsonify(favorite=favorite.serialize())

        # RETURNS THE SERIALIZED GAME AND STATUS 201
        return (response_json, 201)
    else:
        flash('You must be logged in to view')
        return redirect('/login')
        
@app.route('/api/favorite/<slug>', methods=['DELETE'])
def delete_favorite(slug):
    '''ROUTE TO DELETE FAVORITED'''

    # CHECK IF USER IS LOGGED IN. IF NOT, REDIRECTS TO LOGIN PAGE
    if 'username' in session:
        username = session['username']
        slug = slug

        # GET THE FAVORITED GAME FILTERING THE DATABASE WITH THE USERNAME AND GAME SLUG.
        # DELETE THE GAME FROM THE DATABASE
        favorite = Collection.query.filter_by(username=username).filter_by(game_slug=slug).first()

        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify(message='Deleted')
    else:
        flash('You must be logged in to view')
        return redirect('/login')