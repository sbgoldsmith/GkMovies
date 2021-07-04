from app import db
from app.models import User, UserColumn, UserMovie, ImdbMovie, ImdbPlot, GenreMovie, PersonMovie, Person, ClubUserMovie
from Library.DbModule import Dber
from Library.LoggerModule import Timer, info
from Library.ConstantsModuleF import Constants
from Library.FlaskModule import Flasker
import cProfile
import io
import pstats
import contextlib
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from Library.BeanModule import Cuser

@contextlib.contextmanager
def profiled():
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    # uncomment this to see who's calling what
    # ps.print_callers()
    #prnt(s.getvalue())
        

class Display(Constants):
    def reverse(self, orderDir):
        if orderDir == 'asc':
            return 'desc'
        else:
            return 'asc'
        
        
        
    def getSort(self, user, cuser, searcher, sortButton):
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
        column = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.displayType == searcher.displayType, UserColumn.name == sortButton).first();
    
        dbType = None 
        if sortButton.startswith("user"):
            if column.dataFormat in ["number", "currency", "integer", "comma"]:
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
    
    def displayMovies(self, user, cuser, searcher, sortButton):       
        columnSort = self.getSort(user, cuser, searcher, sortButton)
        query = UserMovie.query.filter(UserMovie.user_type == cuser.user_type, UserMovie.user_id == cuser.user_id, UserMovie.displayType == searcher.displayType)

        for userColumn in self.userColumns:
            uSearch = searcher.op(userColumn)
            
            if uSearch:
                column = getattr(UserMovie, userColumn)
                query = query.filter(column.like(uSearch))
   
        movies = query.\
            join(ImdbMovie).\
            join(GenreMovie).\
            join(ImdbPlot)

        if self.isShowPersons(cuser, searcher.displayType):
            movies = movies.join(PersonMovie).join(Person)
            
            ''''
            personMovieActor = aliased(PersonMovie)
            personMovieCrew = aliased(PersonMovie)

            movies = movies.join(personMovieActor)
            movies = movies.join(personMovieCrew)
            movies = movies.join(Person)
            '''
            
        movies = searcher.search(movies, UserMovie.my_date_seen)
        movies = searcher.search(movies, UserMovie.my_rating)
        movies = searcher.search(movies, UserMovie.my_review)
        movies = searcher.search(movies, ImdbMovie.title)
        movies = searcher.search(movies, ImdbMovie.series)
        movies = searcher.search(movies, ImdbPlot.outline)
        movies = searcher.search(movies, ImdbPlot.summary)      
        movies = searcher.search(movies, GenreMovie.genre)
        movies = searcher.search(movies, UserMovie.dateAdded)
        
        if searcher.op('series') and searcher.seriesFirst:
            columnSort = ImdbMovie.seriesSeq
            searcher.seriesFirst = False  
        
        if searcher.op('actor'):   
            movies = movies.filter(Person.name.like(searcher.op('actor'))).filter(PersonMovie.role == 'actor')
        if searcher.op('crew'):   
            movies = movies.filter(Person.name.like(searcher.op('crew'))).filter(PersonMovie.role != 'actor')
                                       

        movies = movies.order_by(columnSort).order_by(ImdbMovie.title).all()

        
        '''
        movies = query.\
            join(ImdbMovie).\
            join(GenreMovie).\
            join(PersonMovie).\
            join(Person).\
            join(ImdbPlot).\
            order_by(ImdbMovie.title)
        prnt(str(movies.statement.compile()))
        '''        
        
        return movies

    def isShowPersons(self, cuser, displayType):

        cols = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.displayType == displayType).all()
        show = 0
        for col in cols:
            if col.name == 'actor' or col.name == 'crew':
                if col.vis == 'T':
                    show += 1
                    
        return show > 0
    
        #cols = UserColumn.query.filter(UserColumn.user_id == user,  (UserColumn.name == 'actor') | (UserColumn.name == 'crew') ).all()

        stop = 1
        
    def getCast(self, user, displayType):
        timer = Timer(cumu=False)
        q = {}
        db = Dber()
        conn = db.getConnection()
        sql = '''select im.tt, pm.nm, name
from user_movie um
left join imdb_movie im on um.imdb_movie_id = im.id
left join person_movie pm on im.tt = pm.tt
left join person p on pm.nm = p.nm
where user_id = 2 and role = 'actor' and srt <= 10 order by tt, srt;
'''
        rs = conn.execute(sql)
        for row in rs:
            tt = row['tt']
            nm = row['nm']
            name = row['name']
            
            if not tt in q:
                tt_list = []
                q[tt] = tt_list
                
            tup = (nm, name)
            q[tt].append(tup)
        
        timer.elapse('getCast make cache')
        return q
    
        
    def getNumCast(self, cuser, displayType):

        q = {}
        db = Dber()
        conn = db.getConnection()
        sql = '''
        select im.tt, count(1) as cnt from user_movie um
left join imdb_movie im on um.imdb_movie_id = im.id
left join person_movie pm on im.tt = pm.tt
where user_type = ''' + "'" + cuser.user_type + "' and user_id = " + str(cuser.user_id) + " and displayType = '" + displayType + "' and role = 'actor' group by im.tt;"

        rs = conn.execute(sql)
        
        for row in rs:
            q[row['tt']] = row['cnt']
        
   
        return q
    
    
    def deleteMovie(self, cuser, imdb_movie_id):
        userMovie = UserMovie.query.filter(UserMovie.user_type == cuser.user_type, UserMovie.user_id == cuser.user_id, UserMovie.imdb_movie_id == imdb_movie_id).first()
        clubUserMovies = ClubUserMovie.query.filter(ClubUserMovie.user_movie_id).all()
        
        for clubUserMovies in clubUserMovies:
            db.session.delete(clubUserMovies)
             
        db.session.delete(userMovie)
        db.session.commit()
            
    def seen(self, cuser, tt):     
        imdbMovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
        userMovie = UserMovie.query.filter(UserMovie.user_type == cuser.user_type, UserMovie.user_id == cuser.user_id, UserMovie.imdb_movie_id == imdbMovie.id).first()
        userMovie.displayType = 'seen'
        db.session.commit()
        return userMovie

     
    def allCast(self, tt):
        #rtn = "<div class='scrollable' style='height:100%'>\n"
        rtn = "<table cellspacing='0' cellpadding='0' style='border:0;'>\n"
        personMovies = PersonMovie.query.filter(PersonMovie.tt == tt, PersonMovie.role == 'actor').order_by(PersonMovie.srt).all()
        for personMovie in personMovies:
            rtn += "<tr style='background-color:transparent;'>\n"
            rtn += "<td style='border:0;text-align:left;width:30px;'>\n"
            rtn += "<a href='https://www.imdb.com/name/" + personMovie.nm + "'  target='_blank'><img src='/static/images/imdb.jpg' style='width:25px'></a>\n"
            rtn += "</td>\n"
            rtn += "<td style='border:0;text-align:left;'>\n"
            rtn += "<a href='Javascript:searchActor(\"" +  personMovie.person.name + "\")' class='imdb'>" + personMovie.person.name + "</a>\n"
            rtn += "</td>\n"
            rtn += "</tr>\n"
        rtn += "</table>\n"
        #rtn += "</div>"
        return rtn
    
    
        
        
        