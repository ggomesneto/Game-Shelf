# GAME SHELF - CAPSTONE PROJECT - GERALDO GOMES
---
![Main Page](https://github.com/ggomesneto/capstone1/blob/main/Game%20Shelf.jpeg)

## ABOUT ME

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

### THE SITE

**GAME SHELF** is a game library that shows information about games, platforms, game genres and more specific data, such as game released date, or developers name. The users will be able to search for the information they need, create an account and post reviews, rate games and add games to their personal collection.

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

	"""Models for database"""
	from flask_sqlalchemy import SQLAlchemy

	db = SQLAlchemy()

	def connect_db(app):
    	db.app = app
    	db.init_app(app)


	class User(db.Model):

    	__tablename__ = 'users'

    	username = db.Column(db.Text, primary_key=True)
    	first_name = db.Column(db.Text, nullable=False)
    	last_name = db.Column(db.Text, nullable=False)
    	email = db.Column(db.Text, nullable=False)

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
