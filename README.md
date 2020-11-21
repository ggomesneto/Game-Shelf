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

 
## API: 
**https://rawg.io/apidocs**

## Database draft:

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
    	dob = db.Column(db.Date)
    	email - db.Column(db.Text, nullable=False)

    	favorites = db.relationship('Collection')
    	reviews = db.relationship('Review')

    	def __repr__(self):
        	return f"<User {self.username} {self.first_name} {self.last_name}>"

	class Collection(db.Model):

    	__tablename__ = 'collections'

    	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    	username = db.Column(db.Text, db.ForeignKey('User.username'))
    	game_slug = db.Column(db.Text, nullable=False)

    	def __repr__(self):
        	return f"<favorite {self.username} {self.game_slug}"

	class Review(db.Model):

    	__tablename__ = 'reviews'

    	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    	username = db.Column(db.Text, db.ForeignKey('User.username'))
    	game_slug = db.Column(db.Text, nullable=False)
