from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'index'
mail = Mail(app)

from app import routes, models

#---------------------+

'''
from app.models import User, UserColumn, ImdbMovie
from app.Imdb import ImdbFind
from datetime import datetime
from Library.AdderModuleF import Adder
from Library.FlaskModule import FlaskHelper
from Library.ServerModule import Inputter
from sqlalchemy.orm import selectinload, joinedload, query
from app.email import send_email, send_password_reset_email


user = User.query.filter_by(login = 'sbg').first()
imdbFind = ImdbFind()
imdbFind.findMovies(user, 'The Godfather')
stop = 1

        
        


user.admin = 'T'
db.session.commit()





args = {'sortButton':'user01', 'titleSearch': 'star',  'reviewSearch': '', 'genreSearch': '', 'actorSearch':'', 'plotSearch':'', 'user01Search':'11'}
user = User.query.filter_by(login = 'tara').first() 


movies = imdbFind.displayMovies(user, args) 
 
for movie in movies:
    
    for actor in movie.imdb_movie.actor_movies:
        print('nm=' + actor.nm)
        print("actor=" + actor.actor.actor)

            


column = UserColumn.query.filter(UserColumn.user_id == 4, UserColumn.name == 'imdbVotes').all();
cols = UserColumn.query.filter(User.login == 'tara', UserColumn.name == 'user02').first();
for col in cols:
    if col.name == 'user02':
        print(col.dataFormat)


stop = 1
    

flasker = FlaskHelper()
flasker.setArgs(user, None)
flasker.resetSort()





inputter = Inputter()
message = inputter.processSettingsDisplayInput(user, 'poster', 'label', 'Hello')



user = User.query.filter_by(login = 'tara').first() 
imdbFind = ImdbFind()
imdbFind.deleteMovie(user, 939)


adder = Adder()
message = imdbFind.updateMovies(1, 20)
#imovie = ImdbMovie.query.filter_by(tt = 'tt0081109').first()
#adder.updateImdbMovie(imovie)




flasker = FlaskHelper()
flasker.setArgs(user, args)
for movie in movies:
    
    for actor in movie.imdb_movie.actor_movies:
        print('nm=' + actor.nm)
        print("actor=" + actor.actor.actor)

            
            
    for col in user.columns:
        rtn = flasker.getCell(col, movie)




'''