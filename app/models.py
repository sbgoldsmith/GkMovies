from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#from django.template.defaultfilters import title
from datetime import datetime
import math
from Library.ConstantsModuleF import Constants
from time import time
import jwt
from app import app

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    cols = 0;
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    login = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    firstName = db.Column(db.String(32))
    lastName = db.Column(db.String(32))
    order_by = db.Column(db.String(12))
    order_dir = db.Column(db.String(6))
    admin = db.Column(db.String(1))
    last_visit = db.Column(db.DateTime())
    movies = db.relationship('UserMovie',  lazy='dynamic')
    columns = db.relationship("UserColumn", lazy='dynamic', order_by="UserColumn.srt")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def setLastVisit(self):
        self.last_visit =  datetime.utcnow()
        db.session.commit()

    def getTableWidth(self):
        rtn = 0
        self.cols = 0;
        for column in self.columns:
            if column.vis == 'T':
                rtn += column.cols
                self.cols += 1
        return math.floor(rtn * Constants().widthFactor)
    

    def getNumCols(self):
        return self.cols

   
    def hasMovie(self, tt):
        im = ImdbMovie.query.filter_by(tt = tt).first()
        if im == None:
            return False
        
        um = UserMovie.query.filter_by(user_id = self.id, imdb_movie_id = im.id).first()   
         
        return  um != None
    
    def get_reset_password_token(self, expires_in=86400):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)            
    
    def __repr__(self):
        return '<User {}, Email is {}>'.format(self.login, self.email)
    

def load_adder_column(id):
    return AdderColumn.query.get(int(id))

class AdderColumn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    width = db.Column(db.Integer)
    align = db.Column(db.String(6))
    valign = db.Column(db.String(8))
    srt = db.Column(db.Integer)

def load_user_movie(id):
    return UserMovie.query.get(int(id))


class UserMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    imdb_movie_id = db.Column(db.Integer, db.ForeignKey('imdb_movie.id'), index=True)
    user01 = db.Column(db.Text())
    user02 = db.Column(db.Text())
    user03 = db.Column(db.Text())
    user04 = db.Column(db.Text())
    user05 = db.Column(db.Text())
    user06 = db.Column(db.Text())
    user07 = db.Column(db.Text())
    user08 = db.Column(db.Text())
    user09 = db.Column(db.Text())
    user10 = db.Column(db.Text())
    imdb_movie = db.relationship('ImdbMovie')

    
def load_imdb_movie(id):
    return ImdbMovie.query.get(int(id))
    
    
class ImdbMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), index=True, unique=True )
    title = db.Column(db.String(255))
    iyear = db.Column(db.Integer)
    runtime = db.Column(db.Time())
    imdbRating = db.Column(db.Float())
    imdbVotes = db.Column(db.Integer())
    plot = db.Column(db.Text())
    poster = db.Column(db.String(255))
    poster_valid =  db.Column(db.String(1))
    genres = db.relationship('GenreMovie', order_by="GenreMovie.srt")
    actor_movies = db.relationship('ActorMovie', order_by="ActorMovie.srt")
        
def load_genre_movie(id):
    return GenreMovie.query.get(int(id))  
    
class GenreMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), db.ForeignKey('imdb_movie.tt'), index = True)
    genre = db.Column(db.String(16))
    srt = db.Column(db.Integer)
    

def load_actor_movie(id):
    return ActorMovie.query.get(int(id))  
    
class ActorMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), db.ForeignKey('imdb_movie.tt'), index = True)
    nm = db.Column(db.String(16), db.ForeignKey('actor.nm'), index=True)
    srt = db.Column(db.Integer)
    actor = db.relationship('Actor')
    
def load_actor(id):
    return Actor.query.get(int(id))  
    
class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nm = db.Column(db.String(16), index=True,  unique=True)
    actor = db.Column(db.String(48))
    
def load_user_column(id):
    return UserColumn.query.get(int(id))

class UserColumn(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    name = db.Column(db.String(16), index = True)
    label = db.Column(db.String(16))
    cols = db.Column(db.Integer)
    rows = db.Column(db.Integer)
    dataFormat = db.Column(db.String(8))
    vis = db.Column(db.String(1))
    srt = db.Column(db.Integer)
    attribute = db.relationship('ColumnAttribute',  uselist=False, back_populates='user_column')
    
    def getWidth(self):
        return math.ceil(self.cols * Constants().widthFactor)

    
def load_column_attribute(id):
    return UserColumn.query.get(int(id))

class ColumnAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), db.ForeignKey('user_column.name'), index = True)
    align = db.Column(db.String(6))
    valign = db.Column(db.String(8))
    sortable = db.Column(db.String(1))
    searchable = db.Column(db.String(1))
    scrollable = db.Column(db.String(1))
    editable = db.Column(db.String(1))
    dataType = db.Column(db.String(6))
    ordr = db.Column(db.Integer)
    user_column = db.relationship("UserColumn", back_populates='attribute')
        
class UrlMovie():
    tt = ''
    title = ''
    iyear = 0
    plot = ""
    countries = []
    button = False