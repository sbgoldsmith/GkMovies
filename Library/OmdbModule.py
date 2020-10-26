import urllib
import requests
from app.models import User, UserColumn, UrlMovie, UserMovie, ImdbMovie, GenreMovie, PersonMovie, Person
from Library.HelperModuleF import getItemList, getImageUrl
from Library.PosterModule import Poster
from Library.ConstantsModuleF import Constants
from flask_login import current_user
from app import db
from Library.LoggerModule import info
from spellchecker import SpellChecker
import re
from app.email import send_email

MAXSPELL = 4



def getWords(titleSearch):
    rtn = []
    str = titleSearch.strip();
    
    index = str.find(' ')
    while index > 0:
        word = str[0:index]
        rtn.append(word)
        
        str = str[index:len(str)].strip()
        index = str.find(' ')
    
    rtn.append(str)  
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
         
class Omdb(Constants):
    def initSpell(self, titleSearch):
        #
        #  First, create spell checker results
        #
        speller = SpellChecker()
        words = getWords(titleSearch)
        self.badWord = ''
        for word in words:
            word = re.sub(r'\W+', '', word)

            self.candidates = speller.candidates(word)
            if word in self.candidates:
                #
                # remove the word given because we don't want to give it back as a candidte
                #
                self.candidates.remove(word)

            if len(self.candidates) > MAXSPELL:
                #
                # Too many word candidates
                #
                self.candidates = []

            if len(self.candidates) > 0:
                #
                #  Found candidates.  Use this and return
                #
                self.badWord = word
                info('Found ' + str(len(self.candidates)) + ' spelling candidates for ' + self.badWord)
                return
            
            
    def find(self, user, titleSearch):
        poster = Poster()
        
        movies = []
        info("titleSearch='" + str(titleSearch) + "'")

        if len(titleSearch) < 3:
            return movies;
        
        if titleSearch.startswith('tt'):
            surl = "http://www.omdbapi.com/?apikey=4bcae80b&i=" + titleSearch
            r = requests.get(url = surl)
            dmovie = r.json()
            urlMovie = self.upopulate(poster, user, dmovie)
            movies.append(urlMovie)
            
        else:
            self.initSpell(titleSearch)   
    
            surl = "http://www.omdbapi.com/?apikey=4bcae80b&type=movie&s=" + str.replace(titleSearch, " ", "+")
            r = requests.get(url = surl) 
            
            if not "Search" in r.json():
                return movies
            
            jmovies = r.json()['Search']
    
            
            for jmovie in jmovies:
                surl = "http://www.omdbapi.com/?apikey=4bcae80b&i=" + jmovie['imdbID']
                r = requests.get(url = surl) 
                try:
                    dmovie = r.json()
                except:
                    #
                    # Skip over any movie that can not be parsed
                    #
                    continue
                
                urlMovie = self.upopulate(poster, user, dmovie)
                
                movies.append(urlMovie)
             
             
        return movies
    
    
    def upopulate(self, poster, user, dmovie):

            
            tt = dmovie['imdbID']
            #poster.addMoviePoster(tt, getImageUrl(dmovie), None)
             
            urlMovie = UrlMovie()
            urlMovie.tt = tt
            urlMovie.title = dmovie['Title']
            urlMovie.iyear = dmovie['Year']
            urlMovie.plot = dmovie['Plot']
            urlMovie.actors = getItemList(dmovie['Actors'])
            urlMovie.countries = getItemList(dmovie['Country'])
            urlMovie.displayType = user.getDisplayType(dmovie['imdbID'])
            urlMovie.genres = getItemList(dmovie['Genre'])
            urlMovie.poster = getImageUrl(dmovie)
            
            return urlMovie
           
            
    def getRottenRatings(self, tt):
        surl = "http://www.omdbapi.com/?apikey=4bcae80b&plot=full&i=" + tt
        r = requests.get(url = surl) 
        movie = r.json()
 
        ratings = movie['Ratings']
    
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
    
    
        return rotten
        
   