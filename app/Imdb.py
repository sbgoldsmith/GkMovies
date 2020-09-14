import urllib
import requests
from app.models import User, UserColumn, UrlMovie, UserMovie, ImdbMovie, GenreMovie, ActorMovie, Actor
from Library.HelperModuleF import getTable, getItemList
from Library.AdderModuleF import Adder
from Library.ConstantsModuleF import Constants
from flask_login import current_user
from app import db
from Library.LoggerModule import info
from spellchecker import SpellChecker
import re

MAXSPELL = 4

def reverse(orderDir):
    if orderDir == 'asc':
        return 'desc'
    else:
        return 'asc'

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
    

            
            
def getSort(user, sortButton):   
    if sortButton != None:
        #Sort button pressed.  Determine new sort and update User table
        if sortButton == user.order_by:
            #Same button so reverse direction
            orderDir = reverse(user.order_dir)
        else:
            #new sort
            if sortButton == 'title':
                orderDir = 'asc'
            else:
                orderDir = 'desc'
        
        user.query.filter_by(id = user.id).update({User.order_by: sortButton, User.order_dir: orderDir})
        db.session.commit()
    else:
        #Nothing pressed, use values from User table
        sortButton = user.order_by
        orderDir = user.order_dir


    table = getTable(sortButton)
    column = UserColumn.query.filter(UserColumn.user_id == user.id, UserColumn.name == sortButton).first();

    dbType = None
    if column.dataFormat in ["number", "currency", "comma"]:
        dbType = db.Numeric()
    elif column.dataFormat == 'date':
        dbType = db.DateTime()

        
    info('Cast=' + str(dbType))

    if dbType and user.order_dir == 'desc':
        columnSorted = db.cast(getattr(table, sortButton), dbType).desc()
    elif dbType and user.order_dir == 'asc':
        columnSorted = db.cast(getattr(table, sortButton), dbType)
    elif not dbType and user.order_dir == 'desc':
        columnSorted = getattr(table, sortButton).desc()
    elif not dbType and user.order_dir == 'asc':
        columnSorted = getattr(table, sortButton)

    #columnSorted = get(table, sortButton);  
    return columnSorted


class ImdbFind(Constants):
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
            
            
    def findMovies(self, user, titleSearch):
        adder = Adder()
        
        movies = []
        info("titleSearch='" + str(titleSearch) + "'")

        if len(titleSearch) < 3:
            return movies;
        
        
        self.initSpell(titleSearch)   

        surl = "http://www.omdbapi.com/?apikey=4bcae80b&type=movie&s=" + str.replace(titleSearch, " ", "+")
        r = requests.get(url = surl) 
        
        if not "Search" in r.json():
            return movies
        
        jmovies = r.json()['Search']
  
        for jmovie in jmovies:
            surl = "http://www.omdbapi.com/?apikey=4bcae80b&i=" + jmovie['imdbID']
            r = requests.get(url = surl) 
            dmovie = r.json()
            adder.addMoviePoster(dmovie, None)
             
            urlMovie = UrlMovie()
            urlMovie.tt = jmovie['imdbID']
            urlMovie.title = dmovie['Title']
            urlMovie.iyear = dmovie['Year']
            urlMovie.plot = dmovie['Plot']
            urlMovie.countries = getItemList(dmovie['Country'])
            
            urlMovie.button = not user.hasMovie(jmovie['imdbID'])

            
            movies.append(urlMovie)
        return movies
    
    
    

    def displayMovies(self, user, searcher, sortButton):
   
        columnSort = getSort(user, sortButton)

        query = UserMovie.query.filter(UserMovie.user_id == user.id)
        
        for userColumn in self.userColumns:
            uSearch = searcher.like(userColumn)
            
            if uSearch:
                column = getattr(UserMovie, userColumn)
                query = query.filter(column.like(uSearch))
   
        movies = query.\
            join(ImdbMovie).\
            join(GenreMovie).\
            join(ActorMovie).\
            join(Actor)

        if searcher.like('title'):
            movies = movies.filter(ImdbMovie.title.like(searcher.like('title')))
        if searcher.like('series'):
            movies = movies.filter(ImdbMovie.series.like(searcher.like('series')))
            if searcher.seriesFirst:
                columnSort = ImdbMovie.seriesSeq
                searcher.seriesFirst = False
        if searcher.like('plot'):
            movies = movies.filter(ImdbMovie.plot.like(searcher.like('plot')))
        if searcher.like('genre'):
            movies = movies.filter(GenreMovie.genre.like(searcher.like('genre')))
        if searcher.like('actor'):   
            movies = movies.filter(Actor.actor.like(searcher.like('actor')))

            
        movies = movies.order_by(columnSort).\
            order_by(ImdbMovie.title).\
            all()
            
        '''
        movies = query.\
            join(ImdbMovie).\
            join(GenreMovie).\
            join(ActorMovie).\
            join(Actor).\
            order_by(ImdbMovie.title).\
            all()
        prnt (str(movies.statement.compile()))
        '''            
            

        info('Found # Movies=' + str(len(movies)))

        return movies
    
    def updateMovies(self, fromMovie, toMovie, doGenres, doCast):
        
        adder = Adder();

        if fromMovie.data == None:
            offset = 0
        else:
            offset = fromMovie.data - 1
               
        if toMovie.data == None:
            limit = 99999
        else: 
            limit = toMovie.data - offset
            

        imovies = ImdbMovie.query.order_by(ImdbMovie.title).offset(offset).limit(limit).all()

        upd = 0
        tot = 0
        for imovie in imovies:
            upd += adder.updateImdbMovie(imovie, doGenres, doCast)
            tot += 1
            
            
        return "Updated " + str(upd) + " of " + str(tot) + " movie records"


    def updateMovie(self, tt, doGenres, doCast):
        imovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
        adder = Adder();
        adder.updateImdbMovie(imovie, doGenres, doCast)
        return imovie
        
     
    def deleteMovie(self, user, imdb_movie_id):
        userMovie = UserMovie.query.filter(UserMovie.user_id == user.id, UserMovie.imdb_movie_id == imdb_movie_id).first()
    
        db.session.delete(userMovie)
        db.session.commit()
        
        

        
        
        
        