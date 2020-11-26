# GAME SHELF - CAPSTONE PROJECT - GERALDO GOMES
---
![Main Page](https://github.com/ggomesneto/capstone1/blob/main/Game%20Shelf.jpeg)

## ABOUT THE PROJECT

The intention of this project is to create a Full-Stack application using all the technologies learned up to this point (~35%) on **Springboard's Software Engineering Career Track course**. 

This project, called **GAME SHELF** uses the following technologies:

- HTML
- CSS
- JAVASCRIPT
- JQUERY
- AJAX
- PYTHON 
- FLASK
- JINJA
- WTFORMS
- POSTGRESQL
- SQLALCHEMY

Since this is a student's project, I'll try to comment as much as possible on the code, and an expert eye will notice that the code will have the same process written in different ways. The idea behind that is to show the different possibilities of getting to the same output ( An example is using AJAX to make API calls and also make API requests on the Backend, using FLASK requests ).

## THE SITE

**GAME SHELF** is a game library that shows information about games, platforms, game genres and more specific data, such as game released date, or developers name. The users will be able to search for the information they need, create an account and post reviews, rate games and add games to their personal collection.

## TODO LIST

- [x] ~~MAIN PAGE~~
- [x] ~~GAME PAGE~~
- [x] ~~REVIEWS PAGE~~
- [ ] EDIT REVIEW
- [x] ~~FLASK ROUTES~~
- [ ] USER PROFILE
- [x] ~~DATABASE MODELS~~
- [x] ~~FORM MODELS~~
- [x] ~~LOGIN / AUTHENTICATION / PASSWORD HASHING~~

## USER FLOW

When offline, the user will be able to search for a game, genre or platform, read other people's reviews and check user's collections.
In addition to that, when online, the user will be able to create his/hers own collection and add reviews to the game.

## UNDERSTANDING FUNCTIONALITIES

One of the biggest obstacles I had was to work with the combination of data from the database and from the API. For example, to append the correct button, depending if the user is logged or not, or if the user has that specific game on his/hers collection or not. On the app.py file there is a route exclusively to send the 'logged in' information to the frontend, so the JS functions I wrote could use the right markup to show the game cards. As I said above, I wanted to write different ways of getting the same result, not only to show it is possible but also to learn how to do it.

### PASSWORD PROTECTION

Each password is salted and encrypted using BCrypt, using the wrapper **flask-bcrypt** and the hash is saved on the database. This adds a layer of security to the password and make it harder to be cracked.

### HOW TO RUN THE APP

If you want to download the code and run on your machine, here's what you have to do:
- Install Postgres
- Open your terminal, access psql and create a database called 'gameshelf'

In another terminal, go to the folder where you unziped the code. Run those lines on the terminal:

- python3 -m venv venv              
- source venv/bin/activate          
- pip3 install flask                
- pip3 install flask-debugtoolbar
- pip3 install flask-wtf
- pip3 install psycopg2-binary
- pip3 install flask-sqlalchemy
- pip3 install ipython
- pip3 install requests
- pip3 install flask-bcrypt
- flask run

You will be installing flask, the debugtoolbar, WTforms, SQLAlchemy, ipython, Requests and Flask-Bcrypt.
The last line is to start running the web app. After that you should access the web app using the url address displayed on the terminal.

### REQUIREMENTS

You can find a list of requirements under the requirements.txt file, but I decided to add the list here too.

- backcall==0.2.0
- blinker==1.4
- certifi==2020.11.8
- chardet==3.0.4
- click==7.1.2
- colorama==0.4.3
- decorator==4.4.2
- Flask==1.1.2
- Flask-DebugToolbar==0.11.0
- Flask-SQLAlchemy==2.4.4
- Flask-WTF==0.14.3
- idna==2.10
- ipython==7.18.1
- ipython-genutils==0.2.0
- itsdangerous==1.1.0
- jedi==0.17.2
- Jinja2==2.11.2
- MarkupSafe==1.1.1
- parso==0.7.1
- pickleshare==0.7.5
- prompt-toolkit==3.0.7
- psycopg2-binary==2.8.6
- Pygments==2.7.1
- requests==2.25.0
- SQLAlchemy==1.3.20
- traitlets==5.0.4
- urllib3==1.26.2
- wcwidth==0.2.5
- Werkzeug==1.0.1
- WTForms==2.3.3

 
## API: 
**https://rawg.io/apidocs**

## Database draft:

![Database](https://github.com/ggomesneto/capstone1/blob/main/database.png)
