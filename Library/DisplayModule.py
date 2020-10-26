from app import db
from app.models import User, UserColumn, UserMovie, ImdbMovie, ImdbPlot, GenreMovie, PersonMovie, Person
from Library.DbModule import Dber
from Library.LoggerModule import info
from Library.ConstantsModuleF import Constants

class Display(Constants):
    def reverse(self, orderDir):
        if orderDir == 'asc':
            return 'desc'
        else:
            return 'asc'
        
        
        
    def getSort(self, user, sortButton):   
        if sortButton != None:
            #Sort button pressed.  Determine new sort and update User table
            if sortButton == user.order_by:
                #Same button so reverse direction
                orderDir = self.reverse(user.order_dir)
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
    
        dber = Dber()
        table = dber.getTable(sortButton)
        column = UserColumn.query.filter(UserColumn.user_id == user.id, UserColumn.name == sortButton).first();
    
        dbType = None
        if sortButton.startswith("user"):
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
    
    def displayMovies(self, user, searcher, sortButton):       
        columnSort = self.getSort(user, sortButton)

        query = UserMovie.query.filter(UserMovie.user_id == user.id, UserMovie.displayType == searcher.displayType)
        
        for userColumn in self.userColumns:
            uSearch = searcher.op(userColumn)
            
            if uSearch:
                column = getattr(UserMovie, userColumn)
                query = query.filter(column.like(uSearch))
   
        movies = query.\
            join(ImdbMovie).\
            join(GenreMovie).\
            join(PersonMovie).\
            join(Person).\
            join(ImdbPlot)


        movies = searcher.search(movies, UserMovie.my_date_seen)
        movies = searcher.search(movies, UserMovie.my_rating)
        movies = searcher.search(movies, UserMovie.my_review)
        movies = searcher.search(movies, ImdbMovie.title)
        movies = searcher.search(movies, ImdbMovie.series)
        movies = searcher.search(movies, ImdbPlot.outline)
        movies = searcher.search(movies, ImdbPlot.summary)      
        movies = searcher.search(movies, GenreMovie.genre)
        
        if searcher.op('actor'):   
            movies = movies.filter(Person.name.like(searcher.op('actor'))).filter(PersonMovie.role == 'actor')
        if searcher.op('crew'):   
            movies = movies.filter(Person.name.like(searcher.op('crew'))).filter(PersonMovie.role != 'actor')
                                                      
        if searcher.op('series') and searcher.seriesFirst:
            columnSort = ImdbMovie.seriesSeq
            searcher.seriesFirst = False                              


            
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
        
    def deleteMovie(self, user, imdb_movie_id):
        userMovie = UserMovie.query.filter(UserMovie.user_id == user.id, UserMovie.imdb_movie_id == imdb_movie_id).first()
    
        db.session.delete(userMovie)
        db.session.commit()
            
    def seen(self, user, tt):
        imdbMovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
        userMovie = UserMovie.query.filter(UserMovie.user_id == user.id, UserMovie.imdb_movie_id == imdbMovie.id).first()
        userMovie.displayType = 'seen'
        db.session.commit()
            
        
        