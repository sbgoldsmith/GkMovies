from app import db, login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#from django.template.defaultfilters import title
from datetime import datetime
import math
from Library.ConstantsModuleF import Constants
from time import time
import jwt
from app import app
#from flask_sqlalchemy import SQLAlchemy
from flask import Markup
import os
from sqlalchemy.orm import deferred

#db = SQLAlchemy(app)

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
    city = db.Column(db.String(48))
    state  = db.Column(db.String(2))
    country = db.Column(db.String(2))
    face = db.Column(db.String(255))
    order_by = db.Column(db.String(12))
    order_dir = db.Column(db.String(6))
    admin = db.Column(db.String(1))
    as_login = db.Column(db.String(32))
    user_since = db.Column(db.DateTime())
    last_visit = db.Column(db.DateTime())

    movies = db.relationship('UserMovie',  lazy='dynamic')
    columns = db.relationship("UserColumn", lazy='dynamic', order_by="UserColumn.srt")
    clubs = db.relationship("ClubUser", lazy='select', order_by="ClubUser.date_accepted")
    
    adminLogin = None
    clubInviteStatus = None
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def setLastVisit(self):
        self.last_visit =  datetime.utcnow()
        db.session.commit()

    def getTableWidth(self, cuser, displayType):
        rtn = 0
        self.cols = 0;
        for column in self.getColumns(cuser, displayType):
            if column.vis == 'T':
                rtn += column.cols
                self.cols += 1
        return math.floor(rtn * Constants().widthFactor)
    

    def getNumCols(self):
        return self.cols

    def get_reset_password_token(self, expires_in=86400):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
            
    def log(self, route, action, arg):
        user_log = UserLog(login=self.as_login, 
                    route=route,
                    action=action,
                    arg=str(arg),
                    log_time = datetime.utcnow())
        db.session.add(user_log)
        db.session.commit()
        
    def asLogin(self, orig):
        self.as_login = orig  + "->" + self.login
        db.session.commit()
        
    def logout(self):
        self.as_login = self.login
        db.session.commit()
        
    def getColumns(self, cuser, displayType):
        columns = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.displayType == displayType).order_by(UserColumn.srt).all()
        return columns
    
    def getCol(self, cuser, name, displayType):
        col = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == name, UserColumn.displayType == displayType).first()
        return col
    
    def getFace(self):

        if self.face != '':
            return self.face
        else:
            return "blank.png"   
            
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


def load_state(id):
    return State.query.get(int(id))  

class State(db.Model):
    id_state = db.Column(db.Integer, primary_key=True)
    state_code = db.Column(db.String(2))
    state_name = db.Column(db.String(24))
    srt = db.Column(db.Integer)
    
def load_country(id):
    return State.query.get(int(id))  

class Country(db.Model):
    id_country = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3))
    country_name = db.Column(db.String(48))
    srt = db.Column(db.Integer)
      
def load_contact(id):
    return User.query.get(int(id))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    email = db.Column(db.String(32))
    firstName = db.Column(db.String(32))
    lastName = db.Column(db.String(32))
    subject = db.Column(db.String(64))
    message = db.Column(db.String())
    contact_date = db.Column(db.DateTime())

    def setContactDate(self):
        self.contact_date =  datetime.utcnow()
        db.session.commit()


def load_user_log(id):
    return UserLog.query.get(int(id))

class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    route = db.Column(db.String(64))
    action = db.Column(db.String(64))
    arg = db.Column(db.String(64))
    log_time = db.Column(db.DateTime())


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
    user_type = db.Column(db.String(12), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    imdb_movie_id = db.Column(db.Integer, db.ForeignKey('imdb_movie.id'), index=True)
    #club_user_movie_id = db.Column(db.Integer, index=True)
    displayType = db.Column(db.String(12))
    dateAdded = db.Column(db.Date())

    my_date_seen = db.Column(db.Date())
    my_rating = db.Column(db.Float())
    my_review = db.Column(db.Text())
    
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
    clubUserMovies = db.relationship('ClubUserMovie', lazy='dynamic')
    
def load_imdb_movie(id):
    return ImdbMovie.query.get(int(id))
    
    
class ImdbMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), index=True, unique=True )
    title = db.Column(db.String(255))
    series = db.Column(db.String(24))
    seriesSeq = db.Column(db.Float())
    iyear = db.Column(db.Integer)
    runtime = db.Column(db.Time())
    imdbRating = db.Column(db.Float())
    imdbVotes = db.Column(db.Integer())
    imdbTopRank = db.Column(db.Integer())
    imdbPopular = db.Column(db.Integer())
    rottenTomatoes = db.Column(db.Integer())
    metaScore = db.Column(db.Integer())
    metaReviews = db.Column(db.Integer())
    metaUserScore = db.Column(db.Float())
    metaUserReviews = db.Column(db.Integer())
    oplot = db.Column(db.Text())
    poster = db.Column(db.String(255))
    poster_valid =  db.Column(db.String(1))
    insert_date = db.Column(db.DateTime())
    update_date = db.Column(db.DateTime())
    
    genres = db.relationship('GenreMovie', order_by="GenreMovie.srt")
    #person_movies = db.relationship('PersonMovie', order_by="PersonMovie.srt")
    person_movies = db.relationship('PersonMovie', primaryjoin='and_(ImdbMovie.tt == PersonMovie.tt, PersonMovie.srt <= ' + str(Constants().personLimit) + ')', order_by="PersonMovie.srt")                 
    plot = db.relationship('ImdbPlot', uselist=False)
    numCast = 0;
    
    def getPersons(self, what):
        rtn = []
      
        for personMovie in self.person_movies:
            if personMovie.role != what:
                continue
            
            if not personMovie.person:
                #
                # This could happen if person table is being updated in the background and not yet finished.  Be silent about this.
                continue
            
            urlPerson = UrlPerson()
            urlPerson.nm = personMovie.person.nm
            urlPerson.name = personMovie.person.name
            urlPerson.job = personMovie.job
            rtn.append(urlPerson)
            
        return rtn   
    
    def getNumPersons(self, what): 
        rtn = 0
        for personMovie in self.person_movies:
            if personMovie.person and personMovie.role == what: 
                rtn += 1
        return rtn
    
    def getGenreList(self):
        rtn = []
        
        for genre in self.genres:
            rtn.append(genre.genre)
        return rtn
    
    def getGenreString(self):
        rtn = ''
        for genre in self.genres:
            rtn += ', ' + genre.genre
            
        return rtn[2:len(rtn)]
    
def load_imdb_plot(id):
    return ImdbPlot.query.get(int(id))

class ImdbPlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), db.ForeignKey('imdb_movie.tt'), index=True, unique=True )
    outline = db.Column(db.Text())
    summary = db.Column(db.Text())

def load_genre(id):
    return Genre.query.get(int(id))  

class Genre(db.Model):
    id_genre = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(24))
    name = db.Column(db.String(24))
    chart = db.Column(db.String(1))
    srt = db.Column(db.Integer)
         
def load_genre_movie(id):
    return GenreMovie.query.get(int(id))  

    
class GenreMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), db.ForeignKey('imdb_movie.tt'), index = True)
    genre = db.Column(db.String(16))
    srt = db.Column(db.Integer)


        
def load_person_movie(id):
    return PersonMovie.query.get(int(id))  
    
class PersonMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tt = db.Column(db.String(16), db.ForeignKey('imdb_movie.tt'), index = True)
    nm = db.Column(db.String(16), db.ForeignKey('person.nm'), index=True)
    role = db.Column(db.String(16))
    job = db.Column(db.String(255))
    srt = db.Column(db.Integer)
    src = db.Column(db.String(6))
    person = db.relationship('Person') 
    
    def getUrlPerson(self):           
        urlPerson = UrlPerson()
        urlPerson.nm = self.nm
        urlPerson.job = self.job
        
        if self.person == None:
            urlPerson.name = 'Missing Name'
        else:
            urlPerson.name = self.person.name
        
        return urlPerson
    
def load_person(id):
    return Person.query.get(int(id))  
    
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nm = db.Column(db.String(16), index=True,  unique=True)
    name = db.Column(db.String(48))
    legacyNameText = deferred(db.Column(db.String(48)))
    birthDate =  deferred(db.Column(db.Date()))
    birthPlace = deferred(db.Column(db.String(255)))
    deathDate = deferred(db.Column(db.Date()))
    deathPlace = deferred(db.Column(db.String(255)))
    deathCause = deferred(db.Column(db.String(255)))
    gender = deferred(db.Column(db.String(16)))
    height = deferred(db.Column(db.Float()))
    realName = deferred(db.Column(db.String(48)))
    image_url = deferred(db.Column(db.String(255)))
    insert_time = deferred(db.Column(db.DateTime()))
    
def load_user_column(id):
    return UserColumn.query.get(int(id))

class UserColumn(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(12), index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index = True)
    name = db.Column(db.String(16), index = True)
    label = db.Column(db.String(16))
    displayType = db.Column(db.String(16))
    cols = db.Column(db.Integer)
    rows = db.Column(db.Integer)
    dataFormat = db.Column(db.String(8))
    vis = db.Column(db.String(1))
    srt = db.Column(db.Integer)
    attribute = db.relationship('ColumnAttribute',  uselist=False, back_populates='user_column')
    
    def getWidth(self):
        return math.ceil(self.cols * Constants().widthFactor)

    def getHeight(self):
        return math.ceil(self.rows * Constants().heightFactor)
    
    def getButtonColor(self):
        if self.name == current_user.order_by:
            return "color:red; font-weight:bold;"
        else:
            return ""
    
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
    ordr = db.Column(db.Integer)
    user_column = db.relationship("UserColumn", back_populates='attribute')
    
def load_version(id):
    return Version.query.get(int(id))

class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    install_date = db.Column(db.DateTime())
    version = db.Column(db.String(12))
    summary = db.Column(db.String())
    audience = db.Column(db.String())
    
    def getVersionHtml(self):
        return '/versions/' + self.version + '.html'
    
    def getFormatInstallDate(self):
        rtn = '{d.month}/{d.day}/{d.year}'.format(d=self.install_date)
        return rtn
    
    
class UrlPerson():
    def __init__(self):
        self.nm = ''
        self.name = ''
        self.birthDate = ''
        self.deathDate= ''
        self.job = ''
        self.image = ''

    
    def getDateRange(self):
        if not self.birthDate or self.birthDate == '0000-00-00':
            return ''
        
        rtn =  '{dt.month}/{dt.day}/{dt.year}'.format(dt = self.birthDate)
        
        if self.deathDate and self.deathDate != '0000-00-00':
            rtn += ' - ' + '{dt.month}/{dt.day}/{dt.year}'.format(dt = self.deathDate)
        return rtn


class UrlMovie():
    
    def __init__(self):
        self.tt = ''
        self.seq = 0
        self.title = ''
        self.iyear = 0
        self.actors = []
        self.directors = []
        self.writers = []
        self.genres = []
        self.plot = ""
        self.poster = ''
        self.displayType = None
        self.clubs = []
        
    def hasImdb(self):
        im = ImdbMovie.query.filter(ImdbMovie.tt == self.tt).first()
        rtn = im == None
        return rtn
    
    def displayCrew(self):
        rtn = 'Director(s):<br>\n'
        
        for director in self.directors:
            #rtn += '&nbsp;&nbsp;' + director.name + ' ' + director.nm + '<br>\n'
            rtn += "&nbsp;&nbsp;<a href='https://www.imdb.com/name/" + director.nm + "'  class='imdb' target='_blank'>" + director.name + "</a><br>\n"
        
        rtn += '<br>Writer(s):<br>\n'
        for writer in self.writers:
            #rtn += '&nbsp;&nbsp;' + writer.job + ' ' + writer.name + ' ' + writer.nm + '<br>\n'
            rtn += "&nbsp;&nbsp;" + writer.job + ' ' + "<a href='https://www.imdb.com/name/" + writer.nm + "'  class='imdb' target='_blank'>" + writer.name + "</a><br>\n"

        return rtn
    
    def markCrew(self):
        return Markup(self.displayCrew())
    
    def displayCast(self):
        rtn = ''
        for actor in self.actors:
            if isinstance(actor, str):
                rtn += actor + '<br>\n'
            else:
                rtn += "<a href='https://www.imdb.com/name/" + actor.nm + "'  class='imdb' target='_blank'>" + actor.name + "</a><br>\n"
                        
                        
           
        return rtn
    
    def markCast(self):
        return Markup(self.displayCast())
    
    def displayGenre(self):
        rtn = ''
        for genre in self.genres:
            rtn += genre + '<br>\n'

        return rtn
    
    def markGenre(self):
        return Markup(self.displayGenre())
    
def load_club(id):
    return Club.query.get(int(id))

class Club(db.Model):
    club_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48))
    description = db.Column(db.String(255))
    owner_id = db.Column(db.Integer)
    header = db.Column(db.String(255))
    status = db.Column(db.String(12))
    allow_add_seen = db.Column(db.String(1))
    allow_add_want = db.Column(db.String(1))
    allow_update = db.Column(db.String(1))
    date_created = db.Column(db.DateTime())
    
    clubUsers = db.relationship('ClubUser',  lazy='dynamic')
   
    def getHead(self):

        if self.header != '':
            return self.header
        else:
            return "blank.png"   
            

def load_invite(id):
    return User.query.get(int(id))

class Invite(db.Model):
    invite_id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, index=True)
    to_user_id = db.Column(db.Integer, index=True)
    type = db.Column(db.String(12))
    type_id = db.Column(db.Integer)
    status = db.Column(db.String(12))
    date_sent = db.Column(db.DateTime())
    date_first_read = db.Column(db.DateTime())
    date_changed = db.Column(db.DateTime())
    
def load_club_user(id):
    return ClubUser.query.get(int(id))

class ClubUser(db.Model):
    club_user_id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    status = db.Column(db.String(12))
    date_accepted = db.Column(db.DateTime())
    date_deleted = db.Column(db.DateTime())
    
    club = db.relationship('Club')
    
    def getUserMovie(self, imdb_movie_id):
        userMovie = UserMovie.query.filter(UserMovie.user_type == 'user', UserMovie.user_id == self.user_id, UserMovie.imdb_movie_id == imdb_movie_id).first()
        return userMovie
    
def load_club_user_movie(id):
    return ClubUserMovie.query.get(int(id))

class ClubUserMovie(db.Model):
    club_user_movie_id = db.Column(db.Integer, primary_key=True)
    user_movie_id = db.Column(db.Integer, db.ForeignKey('user_movie.id'), index=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), index=True)

    club = db.relationship('Club')
 
def load_club_cache(id):
    return ClubCache.query.get(int(id))

class ClubCache(db.Model):
    cache_id = db.Column(db.Integer, primary_key=True)
    current_user_id = db.Column(db.Integer, index=True)
    club_id = db.Column(db.Integer, index=True)
    user_type = db.Column(db.String(12))
    user_id = db.Column(db.Integer, index=True)
    user_movie_id = db.Column(db.Integer,  index=True)
    imdb_movie_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(16))
    dataFormat = db.Column(db.String(8))
    value = db.Column(db.String(255))
    cache_time = db.Column(db.DateTime())

    
    
    
    
    
    
    
    
    
    
    