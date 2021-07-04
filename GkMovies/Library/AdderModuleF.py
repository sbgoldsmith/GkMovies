from Library.HelperModuleF import getItemList, getImageUrl, Dget
from Library.ActorModule import Actorer
from Library.LoggerModule import info, warn
from Library.ConstantsModuleF import Constants
from Library.RapidModule import Rapid, getID
from Library.OmdbModule import Omdb
from Library.PosterModule import Poster
from app.models import ImdbMovie, ImdbPlot, Genre, GenreMovie, PersonMovie, UserMovie, UrlMovie
from Library.HelperModuleF import add0
from Library.DbModule import Dber
from app import db
from flask_login import current_user
import threading
import requests
from datetime import datetime
from flask import Markup
import time
from sqlalchemy import and_

def makeMinTime(rmin):
    hr = int(rmin / 60)
    min = rmin - (hr * 60)
    rtn = str(hr) + ':' + add0(min) + ':00'
    return rtn

    
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



                

    
class Rtn:
    def __init__(self):
        self.dmovie = None
        self.meta = None
        self.imovie = None
        self.iplot = None

class Differ():
    def __init__(self, current, mostRecent):
        self.current = current
        self.mostRecent = mostRecent
        self.results = []
        
    def diffUpdate(self, name):
        currentValue = getattr(self.current, name)
        mostRecentValue = getattr(self.mostRecent, name)
        
        if currentValue == mostRecentValue:
            return 0
        else:
            setattr(self.current, name, mostRecentValue)
            self.results.append(name)
            return 1
        
        
class Adder(Constants):
    def __init__(self):
        x = 1
        
    def updatePersons(self, tt):
        rapid = Rapid()
        urlMovie = UrlMovie()
        rapid.setCast(urlMovie, tt)
            

    def addMovie(self, cuser, displayType, tt):
        rtn = self.addImdbMovie(tt)
        if displayType != 'imdb':
            self.addMovieToUser(cuser, rtn.imovie, displayType)

        
        rapid = Rapid()
        urlMovie = UrlMovie()
        rapid.setMoviePersonsDb(urlMovie, tt)
        rapid.setPlotDb(urlMovie, tt)

        response = {'plot':urlMovie.plot, 'cast': urlMovie.displayCast(), 'crew': urlMovie.displayCrew()}
        return response
      
      
    def addImdbMovie(self, tt, dothread=True):
        info('Adding Imdb, tt=' + tt)
        imovie = ImdbMovie.query.filter_by(tt = tt).first()
        iplot = ImdbPlot.query.filter_by(tt = tt).first()
        
        rapid = Rapid()
        
        if not imovie or not imovie.insert_date or not iplot or iplot.outline == '' or  iplot.summary == '':
            info('Adding Imdb, tt=' + tt + ' not loaded or missing data')
            rtn = self.getImdbDataFields(tt, True)
            d = Dget(rtn.dmovie)
            m = Dget(rtn.meta)
            
            if not imovie:
                #
                # insert Imdb_movie
                #
                rtn.imovie.insert_date = datetime.utcnow()
                db.session.add(rtn.imovie)
            else:
                #
                # update imdb_movie
                #
                self.putImdbFields(tt, imovie, d, m)
                if not imovie.insert_date:
                    imovie.insert_date = datetime.utcnow() 
                imovie.update_date = datetime.utcnow()  

                
            if not iplot:
                db.session.add(rtn.iplot)
            else:
                self.putIplotFields(tt, iplot, d)

            poster = Poster()
            poster.addMoviePoster(tt, getImageUrl(rtn.dmovie['title']), imovie)
            
            db.session.commit()
            rtn.imovie = ImdbMovie.query.filter_by(tt = tt).first()
            

        
        else:
            info('Adding Imdb, tt=' + tt + ' previously loaded')
            rtn = Rtn()
            rtn.imovie = imovie
            rtn.iplot = iplot   
            
        genres = GenreMovie.query.filter(GenreMovie.tt == tt).all()
        if len(genres) == 0:
            self.addMovieGenres(tt, rtn.dmovie.get('genres'))
            db.session.commit()
        
        persons = PersonMovie.query.filter(PersonMovie.tt == tt).all()
        if len(persons) < 5:
            urlMovie = UrlMovie()
            rapid.setCrew(urlMovie, tt)
            
            if dothread:
                threader = threading.Thread(target=self.updatePersons, args=(tt,))
                threader.start()
            else:
                self.updatePersons(tt)
            #
            # give enough time for at least a few persons to be populated
            #
            #time.sleep(5)
        
        return rtn

   
    def getImdbDataFields(self, tt, doMeta):
        rapid = Rapid()

        rtn= Rtn()
        
        rtn.dmovie = rapid.getEndPoint('title/get-overview-details', tt)
        d = Dget(rtn.dmovie)
        #rtn.dmovie = {'id': '/title/tt0448115/', 'title': {'@type': 'imdb.api.title.title', 'id': '/title/tt0448115/', 'image': {'height': 1437, 'id': '/title/tt0448115/images/rm1575720705', 'url': 'https://m.media-amazon.com/images/M/MV5BOWZhZjE4NGQtODg5Ni00MjQ1LWJmMzAtNzQ2N2M1NzYzMDJkXkEyXkFqcGdeQXVyMjMwNDgzNjc@._V1_.jpg', 'width': 970}, 'runningTimeInMinutes': 132, 'title': 'Shazam!', 'titleType': 'movie', 'year': 2019}, 'certificates': {'US': [{'certificate': 'PG-13', 'certificateNumber': 52028, 'ratingReason': 'Rated PG-13 for intense sequences of action, language, and suggestive material', 'ratingsBody': 'MPAA', 'country': 'US'}]}, 'ratings': {'canRate': True, 'rating': 7.1, 'ratingCount': 243015, 'topRank': 2101}, 'genres': ['Action', 'Adventure', 'Comedy', 'Fantasy'], 'releaseDate': '2019-04-05', 'plotOutline': {'id': '/title/tt0448115/plot/po4016727', 'text': 'A newly fostered young boy in search of his mother instead finds unexpected super powers and soon gains a powerful enemy.'}, 'plotSummary': {'author': 'Kenneth Chisholm (kchishol@rogers.com)', 'id': '/title/tt0448115/plot/ps4470004', 'text': "In Philadelphia, Billy Batson is an abandoned child who is proving a nuisance to Child Services and the authorities with his stubborn search for his lost mother. However, in his latest foster home, Billy makes a new friend, Freddy, and finds himself selected by the Wizard Shazam to be his new champion. Now endowed with the ability to instantly become an adult superhero by speaking the wizard's name, Billy gleefully explores his new powers with Freddy. However, Billy soon learns that he has a deadly enemy, Dr. Thaddeus Sivana, who was previously rejected by the wizard and has accepted the power of the Seven Deadly Sins instead. Now pursued by this mad scientist for his own power as well, Billy must face up to the responsibilities of his calling while learning the power of a special magic with his true family that Sivana can never understand."}}
        tt = getID(rtn.dmovie['id'])
        #j = rapid.getEndPoint('title/get-genres', tt)

        if doMeta:
            rtn.meta = rapid.getEndPoint('title/get-metacritic', tt)
            m = Dget(rtn.meta)
        else:
            m = None
        #rtn.meta = {'@type': 'imdb.api.title.metacritic', 'id': '/title/tt0448115/', 'metaScore': 71, 'metacriticUrl': 'https://www.metacritic.com/movie/shazam!?ftag=MCD-06-10aaa1c', 'reviewCount': 53, 'userRatingCount': 1241, 'userScore': 7.6}


       
       
        
        rtn.imovie = ImdbMovie()
        self.putImdbFields(tt, rtn.imovie, d, m)
        
        rtn.iplot = ImdbPlot()
        self.putIplotFields(tt, rtn.iplot, d)

        
        return rtn
    
    def putImdbFields(self, tt, imovie, d, m):
        imovie.tt = tt
        imovie.title = d.get('title', 'title')
        imovie.series = ''
        imovie.seriesSeq = 0
        imovie.runtime = makeMinTime(d.getInt('title', 'runningTimeInMinutes'))
        imovie.iyear = d.getInt('title', 'year')
        imovie.imdbRating = d.getFloat('ratings','rating')
        imovie.imdbVotes = d.getInt('ratings','ratingCount')
        imovie.imdbTopRank = d.getInt('ratings','topRank')
        imovie.imdbPopular = 0
        if m:
            omdb = Omdb()
            imovie.rottenTomatoes = omdb.getRottenRatings(tt)
            imovie.metaScore = m.getInt('metaScore')
            imovie.metaReviews = m.getInt('reviewCount')
            imovie.metaUserScore = m.getFloat('userScore')
            imovie.metaUserReviews = m.getInt('userRatingCount')
            
        imovie.oplot = ''
        imovie.poster = d.get('title', 'image', 'url')
        imovie.poster_valid = str(imovie.poster != '')[0]
        
        
    def putIplotFields(self, tt, iplot, d):
        iplot.tt = tt
        iplot.outline = d.get('plotOutline','text')
        iplot.summary = d.get('plotSummary','text')
        
    def addMovieGenres(self, tt, genres):
        stmt = GenreMovie.__table__.delete().where(GenreMovie.tt == tt)
        db.session.execute(stmt)
        
        srt = 1
        for genre in genres:
            gm = GenreMovie(tt = tt,
                       genre = genre,
                       srt = srt)

            db.session.add(gm)
            srt += 1    


    def addMovieToUser(self, cuser, imovie, displayType):
        umovie = UserMovie.query.filter(UserMovie.user_type == cuser.user_type, UserMovie.user_id == cuser.user_id, UserMovie.imdb_movie_id == imovie.id).first()
        if umovie:
            # setting movie from want to movie_seen
            umovie.displayType = displayType

        else:
            umovie = UserMovie(user_type =  cuser.user_type,
                               user_id = cuser.user_id,
                               imdb_movie_id = imovie.id,
                               displayType = displayType,
                               dateAdded = datetime.utcnow(),
                               
                               my_date_seen = '0000-00-00',
                               my_rating = 0,
                               my_review = '',
                               
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
        return umovie
    
    
    def updateOldestImdbMovies(self, cnt, doGenres, doPersons):
        
        adder = Adder();
        
        sql = '''SELECT * FROM imdb_movie im
order by update_date, insert_date, imdbVotes desc limit ''' + str(cnt) + ';'
        
        db = Dber()
        conn = db.getConnection()
        rs = conn.execute(sql)
        upd = 0
        tot = 0
        
        for row in rs:
            imovie = ImdbMovie.query.filter(ImdbMovie.tt == row['tt']).first()
            results = self.updateImdbMovie(imovie, True, doGenres, doPersons)
            if len(results) > 0:
                info("Updated '" + imovie.title + "' with " + str(len(results)) + " fields.")
                upd += 1
            tot += 1

        return "Updated " + str(upd) + " of " + str(tot) + " movie records"
    
    
    def updateSingleImdbMovie(self, tt, doGenres, doPersons):    
        imovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
        if not imovie:
            rtnm = self.addImdbMovie(tt)
            rtn = "Added '" + rtnm.imovie.title + "':<br>\n"
        else:
            results = self.updateImdbMovie(imovie, True, doGenres, doPersons)
            if len(results) == 0:
                rtn = "No updates needed for '" + imovie.title + "'<br>\n"
            else:
                rtn = "Updated '" + imovie.title + "':<br>\n"
                for fieldName in results:
                    rtn += "&nbsp;&nbsp;&nbsp;&nbsp;" + fieldName + "<br>\n"
        return Markup(rtn)
    
    def updateRankandPopularImdbMovies(self):
        rtn = self.updateRankImdbMovie() + '<br>\n'
        self.noRankDups()
        rtn += self.updatePopularImdbMovie()
        
        return Markup(rtn)
    
        
    def updateRankImdbMovie(self): 
        rapid = Rapid()
        rankList = rapid.getNoIdEndPoint('title/get-top-rated-movies')
        
        updated = 0
        added = 0
        rank = 0
        
        for chart in rankList:
            rank += 1
            tt = getID(chart['id'])
            imovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
            if imovie:
                if imovie.imdbTopRank != rank or str(imovie.imdbRating) != str(chart['chartRating']):
                    imovie.imdbTopRank = rank
                    imovie.imdbRating = chart['chartRating']
                    db.session.commit()
                    updated += 1
            else:
                self.addImdbMovie(tt, dothread=False)
                added += 1
        
        rtn = "Top Rank: Updated " + str(updated) + " and Added " + str(added)
        info(rtn)
        return rtn
    
    def noRankDups(self):
        #
        #    First, get the list of dups
        #
        sql = '''
SELECT imdbTopRank, count(1) as cnt
FROM imdb_movie
WHERE imdbTopRank > 0
GROUP BY imdbTopRank
HAVING cnt > 1'''
        dbr = Dber();
        conn = dbr.getConnection()
        rs = conn.execute(sql)
        
        for row in rs:
            rank = row['imdbTopRank']
            imovies = ImdbMovie.query.filter(ImdbMovie.imdbTopRank == rank).all()
            for imovie in imovies:
                self.updateImdbMovie(imovie, True, False, False)
            
            
        
    def updatePopularImdbMovie(self): 
        #
        #    Zero out last popular movies
        #
        sql = "UPDATE imdb_movie SET imdbPopular = 0;"
        dbr = Dber();
        conn = dbr.getConnection()
        conn.execute(sql)
        db.session.commit()
        
        #
        #    Get current popular movies
        #
        rapid = Rapid()
        popList = rapid.getNoIdEndPoint('title/get-most-popular-movies')
        
        updated = 0
        added = 0
        pop = 0
        
        #
        #    Update or movies as needed
        #
        for id in popList:
            pop += 1
            tt = getID(id)
            imovie = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
            if imovie:
                if imovie.imdbPopular != pop:
                    imovie.imdbPopular = pop
                    db.session.commit()
                    updated += 1
            else:
                rtn = self.addImdbMovie(tt, dothread=False)
                rtn.imovie.imdbPopular = pop
                db.session.commit()
                added += 1
        
        rtn = "Popular: Updated " + str(updated) + " and Added " + str(added)
        info(rtn)
        return rtn
    
    def old_updateRankImdbMovie(self, uptoRank): 
        imovies = ImdbMovie.query.filter(and_(ImdbMovie.imdbTopRank > 0, ImdbMovie.imdbTopRank <= uptoRank)).order_by(ImdbMovie.imdbTopRank).all()
        updates = 0
        for imovie in imovies:
            results = self.updateImdbMovie(imovie, False, False, False)
            
            
            info("Updated #" + str(imovie.imdbTopRank) + " '" + imovie.title + "' with " + str(len(results)) + " fields.")
            if len(results) > 0:
                updates += 1
                
        rtn = "Updated " + str(updates) + " movies"
        return rtn
    
        
    def updateImdbMovie(self, currentMovie, doMeta, doGenres, doPersons):
        results = []

        rtn = self.getImdbDataFields(currentMovie.tt, doMeta)
        
        recentMovie = rtn.imovie
        
        if not doMeta:
            #
            #    Set to old values
            #
            recentMovie.rottenTomatoes = currentMovie.rottenTomatoes
            recentMovie.metaScore = currentMovie.metaScore
            recentMovie.metaReviews = currentMovie.metaReviews
            recentMovie.metaUserScore = currentMovie.metaUserScore
            recentMovie.metaUserReviews = currentMovie.metaUserReviews
         
        recentMovie.imdbPopular = currentMovie.imdbPopular
        mdiff = Differ(currentMovie, recentMovie)

    
        fieldUpdate = 0 

        fieldUpdate += mdiff.diffUpdate('imdbRating')
        fieldUpdate += mdiff.diffUpdate('imdbVotes')
        fieldUpdate += mdiff.diffUpdate('imdbTopRank')
        fieldUpdate += mdiff.diffUpdate('rottenTomatoes')
        fieldUpdate += mdiff.diffUpdate('metaScore')
        fieldUpdate += mdiff.diffUpdate('metaReviews')
        fieldUpdate += mdiff.diffUpdate('metaUserScore')
        fieldUpdate += mdiff.diffUpdate('metaUserReviews')
        fieldUpdate += mdiff.diffUpdate('metaUserReviews')
        fieldUpdate += mdiff.diffUpdate('poster')

        
        currentPlot = ImdbPlot.query.filter(ImdbPlot.tt == currentMovie.tt).first()
        if not currentPlot:
            currentPlot = ImdbPlot(tt = currentMovie.tt)
            db.session.add(currentPlot)
            
        recentPlot = rtn.iplot
        pdiff = Differ(currentPlot, recentPlot)
        fieldUpdate += pdiff.diffUpdate('outline')
        fieldUpdate += pdiff.diffUpdate('summary')
        
        results = mdiff.results + pdiff.results

        
        poster = Poster()
        poster_rtn = poster.addMoviePoster(currentMovie.tt, currentMovie.poster, currentMovie)
        
        
        if doGenres:
            self.addMovieGenres(currentMovie.tt, rtn.dmovie.get('genres'))
            fieldUpdate += 1
        

        if not currentMovie.update_date or fieldUpdate + poster_rtn > 0:
            currentMovie.update_date = datetime.utcnow()
            db.session.commit()
            
        if doPersons:
            rapid = Rapid()
            urlMovie = UrlMovie()
            rapid.setCrew(urlMovie, currentMovie.tt)
            rapid.setCast(urlMovie, currentMovie.tt)


        return results
       

    
    
    