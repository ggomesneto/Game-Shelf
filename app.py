from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

@app.route('/')
def default_page():
    return render_template('index.html')


@app.route('/<genre>')
def genre_route(genre):
    genre_list = ['action', 'strategy', 'rpg', 'shooter', 'adventure', 'puzzle', 'racing', 'sports']
    if genre in genre_list:
        title = genre
    else:   
        title ='not found'
    return  render_template('index.html', title=title)