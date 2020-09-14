from Library.HelperModuleF import getItemList
from Library.ActorModule import Actorer
from Library.LoggerModule import info
from Library.ConstantsModuleF import Constants

from app.models import ImdbMovie, GenreMovie, UserMovie
from app.email import send_email
from Library.HelperModuleF import add0
from app import db
from flask_login import current_user

import urllib
import os 
import requests
from datetime import datetime

def makeTime(strg):
    index1 = str.find(strg, " min")
    if index1 == 0 or strg == "N/A":
        rtn = "0:00:00"
    else:
        index2 = str.find(strg, " h ")
        if index2 == -1:
            min = int(strg[0:index1])
            rtn = str(int(min / 60)) +  ":"  + add0(min % 60) +  ":00"
        else:
            rtn = strg[0:1] + ":" + strg[5:7] + ":00"
            
    return rtn

def makeVotes(strg):
    if strg == 'N/A':
        return 0
    else:
        strg = strg.replace(",", "")
        return int(strg)
    
def makeFloatRating(strg):
    if strg == 'N/A':
        return 0.0
    else:
        strg = strg.replace(",", "")
        return float(strg)

def getRatings(jmovie):
    rtn = []
    ratings = jmovie['Ratings']
    
    rotten = 0;
    meta = 0
    
    for rating in ratings:
        if rating['Source'] == 'Internet Movie Database':
            ignore = 1
        elif rating['Source'] == 'Rotten Tomatoes':
            rotten = makeIntRating(rating['Value'])
        elif rating['Source'] == 'Metacritic':    
            meta = makeIntRating(rating['Value'])
        else:
            src = 'Source = ' + rating['Source']
            send_email("New OMDB Rating", 'steven.bl.goldsmith@gmail.com', 'sgoldsmith@goldkeys.com', src, src) 
    
    rtn.append(rotten)
    rtn.append(meta)
    
    return rtn

                
def makeIntRating(strg):
    if strg == 'N/A':
        return 0
    elif "/" in strg:
        index = strg.find("/")
        rtn = int(strg[0:index])
        return rtn
    else:
        strg = strg.replace("%", "")
        return int(strg)
    
class Rtn:
    def __init__(self):
        self.imovie = None
        self.jmovie = None
    
class Adder(Constants):
    def __init__(self):
        x = 1
        
 
            
    def addMovie(self, tt):
        imovie = self.addImdbMovie(tt)
        self.addMovieToUser(imovie)
   
        return ""
      
    
    def addImdb(self, tt):
        self.addImdbMovie(tt)
   
        return ""
                 
    def addImdbMovie(self, tt):
        imovie = ImdbMovie.query.filter_by(tt = tt).first()

        if imovie == None:
            rtn = self.addMovieToImdb(tt)
            self.addMovieGenres(rtn.jmovie)
            
            actorer = Actorer()
            actorer.addMovieActors(rtn.jmovie)
            imovie = rtn.imovie
            
   
        return imovie
    
    def addMovieToImdb(self, tt):
        rtn = Rtn()
        surl = "http://www.omdbapi.com/?apikey=4bcae80b&plot=full&i=" + tt
        r = requests.get(url = surl) 
        jmovie = r.json()

        ratings = getRatings(jmovie)        
                
        imovie = ImdbMovie(tt = jmovie['imdbID'],
                       title = jmovie['Title'],
                       series = '',
                       seriesSeq = 0,
                       iyear = jmovie['Year'],
                       runtime = makeTime(jmovie['Runtime']),
                       imdbRating = makeFloatRating(jmovie['imdbRating']),
                       imdbVotes = makeVotes(jmovie['imdbVotes']),
                       rottenTomatoes = ratings[0],
                       metaCritic = ratings[1],
                       plot = jmovie['Plot'],
                       poster = jmovie['Poster'],
                       poster_valid = 'T')  #.debug rethink this

        db.session.add(imovie)
        db.session.commit()

        rtn.jmovie = jmovie
        rtn.imovie = imovie
        
        return rtn

    def addMovieGenres(self, jmovie):
        stmt = GenreMovie.__table__.delete().where(GenreMovie.tt == jmovie['imdbID'])
        db.session.execute(stmt)
        db.session.commit()
        
        srt = 1
        for genre in getItemList(jmovie['Genre']):
            gm = GenreMovie(tt = jmovie['imdbID'],
                       genre = genre,
                       srt = srt)

            db.session.add(gm)
            db.session.commit()
            srt += 1    


    def addMovieToUser(self, imovie):    
        umovie = UserMovie(user_id = current_user.id,
                           imdb_movie_id = imovie.id,
                           add_date = datetime.utcnow(),
                           user01 = '',
                           user02 = '',
                           user03 = '',
                           user04 = '',
                           user05 = '',
                           user06 = '',
                           user07 = '',
                           user08 = '',
                           user09 = '',
                           user10 = '')
                               
        db.session.add(umovie)
        db.session.commit()
        
    def updateImdbMovie(self, imovie, doGenres, doCast):
        surl = "http://www.omdbapi.com/?apikey=4bcae80b&plot=full&i=" + imovie.tt
        r = requests.get(url = surl) 
        dmovie = r.json()
        
        rtn = 0       
        ratings = getRatings(dmovie)
        if str(imovie.imdbRating) != str(makeFloatRating(dmovie['imdbRating'])) or \
            str(imovie.imdbVotes) != str(makeVotes(dmovie['imdbVotes'])) or \
            str(imovie.rottenTomatoes) != str(ratings[0]) or \
            str(imovie.metaCritic) != str(ratings[1]) or \
            imovie.plot != dmovie['Plot'] or \
            imovie.poster != dmovie['Poster']:

            imovie.imdbRating = makeFloatRating(dmovie['imdbRating'])
            imovie.imdbVotes = makeVotes(dmovie['imdbVotes'])
            imovie.rottenTomatoes = ratings[0]
            imovie.metaCritic = ratings[1]
            imovie.plot = dmovie['Plot']
            imovie.poster = dmovie['Poster']

            rtn = 1
            
            
        poster_rtn = self.addMoviePoster(dmovie, imovie)
        db.session.commit()
        
        if doGenres:
            self.addMovieGenres(dmovie)
            
        if doCast:
            actorer = Actorer()
            actorer.addMovieActors(dmovie)
        
        if poster_rtn == 1:
            rtn = 1
            
        return rtn

    def addMoviePoster(self, dmovie, imovie):
        rtn = 0;
        imagePath = self.posterPath + dmovie['imdbID'] + ".jpg"
        if imovie != None:
            imovie.poster = dmovie['Poster']
            
        if os.path.exists(imagePath):
            valid = 'T'
         
        elif dmovie['Poster'] == "N/A":
            valid = 'F'
        
        else: 
            try:
                info('Downloading to ' + imagePath)
                urllib.request.urlretrieve(dmovie['Poster'], imagePath)
                valid = 'T'
                rtn = 1
            except:
                info('Could not download ' + dmovie['Poster'])
                valid = 'F'
              
        if imovie != None:
            imovie.poster_valid = valid
            
        return rtn       
