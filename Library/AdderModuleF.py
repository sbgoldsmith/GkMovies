from Library.ConstantsModuleF import *
from Library.HelperModuleF import getItemList
from Library.ActorModule import Actorer

from app.models import ImdbMovie, GenreMovie, UserMovie
from Library.HelperModuleF import add0
from app import db
from flask_login import current_user

import urllib
import os 
import requests

 
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
    
def makeRating(strg):
    if strg == 'N/A':
        return 0.0
    else:
        strg = strg.replace(",", "")
        return float(strg)
    
class Rtn:
    def __init__(self):
        self.imovie = None
        self.jmovie = None
    
class Adder(Constants):
    def __init__(self):
        x = 1
        
 
            
    def addMovie(self, tt):
        imovie = ImdbMovie.query.filter_by(tt = tt).first()

        if imovie == None:
            rtn = self.addMovieToImdb(tt)
            self.addMovieGenres(rtn.jmovie)
            
            actorer = Actorer()
            actorer.addMovieActors(rtn.jmovie)
            imovie = rtn.imovie
            
        self.addMovieToUser(imovie)
   
        return ""
      
    def addMovieToImdb(self, tt):
        rtn = Rtn()
        surl = "http://www.omdbapi.com/?apikey=4bcae80b&plot=full&i=" + tt
        r = requests.get(url = surl) 
        jmovie = r.json()
          
        imovie = ImdbMovie(tt = jmovie['imdbID'],
                       title = jmovie['Title'],
                       iyear = jmovie['Year'],
                       runtime = makeTime(jmovie['Runtime']),
                       imdbRating = makeRating(jmovie['imdbRating']),
                       imdbVotes = makeVotes(jmovie['imdbVotes']),
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
                           seen = '0000-00-00',
                           stars = 0,
                           review = "",
                           user01 = '',
                           user02 = '',
                           user03 = '',
                           user04 = '',
                           user05 = '')
                               
        db.session.add(umovie)
        db.session.commit()
        
    def updateImdbMovie(self, imovie):
        surl = "http://www.omdbapi.com/?apikey=4bcae80b&plot=full&i=" + imovie.tt
        r = requests.get(url = surl) 
        dmovie = r.json()
        
        rtn = 0       
        if str(imovie.imdbRating) != str(makeRating(dmovie['imdbRating'])) or \
            str(imovie.imdbVotes) != str(makeVotes(dmovie['imdbVotes'])) or \
            imovie.plot != dmovie['Plot'] or \
            imovie.poster != dmovie['Poster']:

            imovie.imdbRating = makeRating(dmovie['imdbRating'])
            imovie.imdbVotes = makeVotes(dmovie['imdbVotes'])
            imovie.plot = dmovie['Plot']
            imovie.poster = dmovie['Poster']

            rtn = 1
            
            
        poster_rtn = self.addMoviePoster(dmovie, imovie)
        db.session.commit()
        
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
                print("*** addMoviePoster, trying download to " + imagePath)
                urllib.request.urlretrieve(dmovie['Poster'], imagePath)
                valid = 'T'
                rtn = 1
            except:
                print(dmovie['Poster'])
                valid = 'F'
              
        if imovie != None:
            imovie.poster_valid = valid
            
        return rtn       
