from flask import Flask, request, render_template, redirect, Markup
from flask_debugtoolbar import DebugToolbarExtension
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def default_page():
    '''DEFAULT PAGE WITH FUNCTION TO SEARCH FOR TRENDING GAMES'''
    title = 'NEW AND TRENDING'
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


        return render_template('game_info.html', title=title, platforms=platforms, description=description, genres=genres, developers=developers, esrb_rating=esrb_rating, metacritic=metacritic, publishers=publishers, released=released, website=website, images=images, stores=stores)
    else:
        return redirect('/')
    
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




# ADD TO DATABASE A QUERY THAT SHOWS USERS WITH THE SAME GAMES.MAYBE A PERSONAL CHAT OR SOMETHING


@app.route('/login')
def login_route():

    return render_template('login.html')