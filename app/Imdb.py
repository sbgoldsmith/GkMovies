import urllib
import requests
from app.models import User, UserColumn, UrlMovie, UserMovie, ImdbMovie, GenreMovie, ActorMovie, Actor
from Library.HelperModuleF import getTable, getItemList
from Library.AdderModuleF import Adder
from Library.ConstantsModuleF import Constants
from flask_login import current_user
from app import db



def like(args, strg):
    if strg in args:
        return "%" + args[strg] + "%"
    else:
        return "%"

def reverse(orderDir):
    if orderDir == 'asc':
        return 'desc'
    else:
        return 'asc'
    
    
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
        #user.query.filter_by(login = current_user.login).update({User.order_by: sortButton, User.order_dir: orderDir})
        #user.query.filter_by(login = 'tara').update({User.order_by: sortButton, User.order_dir: orderDir})
        db.session.commit()
    else:
        #Nothing pressed, use values from User table
        sortButton = user.order_by
        orderDir = user.order_dir


    table = getTable(sortButton)
    column = UserColumn.query.filter(UserColumn.user_id == user.id, UserColumn.name == sortButton).first();

    if column.dataFormat in ["number", "currency", "comma"]:
        dbType = db.Float
    elif column.dataFormat == 'date':
        dbType = db.DateTime()
    else:
        dbType = db.String()
        
        
    print("cast = ")
    print(dbType)
    if user.order_dir == 'desc':
        columnSorted = db.cast(getattr(table, sortButton), dbType).desc()
    else:
        columnSorted = db.cast(getattr(table, sortButton), dbType)

            
    return columnSorted


class ImdbFind(Constants):
   
    def findMovies(self, user, titleSearch):
        adder = Adder()
        
        movies = []
        print("==== in findMovies, titleSearch=" + str(titleSearch))
        if len(titleSearch) < 3:
            return movies;
        
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
    
    
    

    def displayMovies(self, user, args):
        sortButton = args.get('sortButton')
        
        titleSearch = like(args, 'titleSearch')
        genreSearch = like(args, 'genreSearch')
        actorSearch = like(args, 'actorSearch')
        plotSearch = like(args, 'plotSearch')
        
        columnSort = getSort(user, sortButton)


        query = UserMovie.query.filter(UserMovie.user_id == user.id)
        for userColumn in self.userColumns:
            sname = userColumn + 'Search'
            uSearch = like(args, sname)
            if uSearch not in ['%', '%%']:
                column = getattr(UserMovie, userColumn)
                query = query.filter(column.like(uSearch))

        movies = query.\
            join(ImdbMovie).\
            filter(ImdbMovie.title.like(titleSearch)).\
            filter(ImdbMovie.plot.like(plotSearch)).\
            join(GenreMovie).\
            filter(GenreMovie.genre.like(genreSearch)).\
            join(ActorMovie).\
            join(Actor).\
            filter(Actor.actor.like(actorSearch)).\
            order_by(columnSort).\
            order_by(ImdbMovie.title).\
            all()
                   
        print("in Imdb.display, titleSearch = :" + titleSearch + ":, movies = " +  str(len(movies)))

        return movies
    
    def updateMovies(self, fromMovie, toMovie):
        
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
            upd += adder.updateImdbMovie(imovie)
            tot += 1
            
            
        return "Updated " + str(upd) + " of " + str(tot) + " movie records"


    def deleteMovie(self, user, imdb_movie_id):
        userMovie = UserMovie.query.filter(UserMovie.user_id == user.id, UserMovie.imdb_movie_id == imdb_movie_id).first()
    
        db.session.delete(userMovie)
        db.session.commit()
        
        
        
        
        
        
        