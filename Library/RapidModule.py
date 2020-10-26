from app import db
from app.models import ImdbMovie, ImdbPlot, PersonMovie, UrlMovie, Person, UrlPerson, Genre, GenreMovie
from Library.ConstantsModuleF import Constants
from Library.PosterModule import Poster
from Library.LoggerModule import info, warn, error, Timer
from Library.HelperModuleF import makeDate, getImageUrl, Dget
import requests
import time
from datetime import datetime
from flask import Markup
import sys

GENRE_MOVIE_LIMIT = 15
URL  = "https://imdb8.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "0079b1e126msh9e9ad2ba4a5bee7p1d8b00jsn472b69b29949"
    }



'''
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "0079b1e126msh9e9ad2ba4a5bee7p1d8b00jsn472b69b29949"
    '''
excludes = ['', 'tvEpisode', 'tvMiniSeries', 'tvSeries', 'tvShort','tvSpecial', 'short', 'video', 'videoGame']

def getID(result):
    
    if isinstance(result, str):
        id = result
    else:
        id = result['id']
        if 'id' in result:
            id = result['id']
        else:
            return None


    i1 = id.find('/', 1)
    i2 = id.rfind('/')
    rtn = id[i1+1:i2]
    
    return rtn



def getIDstr(id):
    i1 = id.find('/', 1)
    i2 = id.rfind('/')
    rtn = id[i1+1:i2]  
    return rtn

    
class Rapid(Constants):
    
    def listMovies(self, user, titleSearch):
        timer = Timer()
        movies = []
        
        results = self.getFind(titleSearch)
                       
        for film in results:

            if not film.get('id').startswith('/title'):
                continue
            
            urlMovie = self.processFilm(user, film)
            if urlMovie:
                movies.append(urlMovie)

        return movies

    def listMoviesByGenre(self, user, genre):
        movies = []
        results = self.getMoviesByGenre(genre)
        i = 0;
        
        for id in results:
            tt = getID(id)
            urlMovie = self.getOrFind(user, tt)
            if urlMovie:
                movies.append(urlMovie)    
                i += 1
                if i >= GENRE_MOVIE_LIMIT:
                    break
            
        return movies
    
    
    def listPersons(self, sperson, lesser):
        timer = Timer()
        persons = []
        
        results = self.getFind(sperson)
                       
        for result in results:
            r = Dget(result)
            
            if r.get('id').startswith('/title'):
                continue
            
            nm = getID(result)
            urlPerson = UrlPerson()
            urlPerson.nm = nm
            urlPerson.name = r.get('legacyNameText')
            
            image_url = r.get('image', 'url')

            if image_url != '' or lesser == 'true':
                urlPerson.image = image_url
                person = Person.query.filter(Person.nm == nm).first()
                persons.append(urlPerson)
                
                #
                # This snippet won't be needed once the image_url's get filled
                #
                if person != None:
                    person.image_url = image_url
                    db.session.commit()
                    
            
        
        return persons
    
    
    def listPerson(self, nm):
      
        persons = []
        
        person = Person.query.filter(Person.nm == nm).first()
        if person == None or person.insert_time == None or person.image_url == '':
            j = self.getEndPoint('actors/get-bio', nm)
            if j != None:
                self.replacePerson(j)
                person = Person.query.filter(Person.nm == nm).first()
                
                

        urlPerson = UrlPerson()
        urlPerson.nm = person.nm
        urlPerson.name = person.name
        urlPerson.birthDate = person.birthDate
        urlPerson.deathDate = person.deathDate
        urlPerson.image = person.image_url
    
        persons.append(urlPerson)
        
        return persons



    def listPersonMovies(self, user, nm):
        movies = []
        timer = Timer()

        j = self.getEndPoint('actors/get-all-filmography', nm)
        films = j['filmography']
        

        for film in films:
            urlMovie = self.processFilm(user, film)
            if urlMovie != None:   
                movies.append(urlMovie)

            
        timer.elapse("personId='" + str(nm) + "'")
        return movies
    
    def getOrFind(self, user, tt):
        imovie = ImdbMovie.query.filter_by(tt = tt).first()
        urlMovie = UrlMovie()
        urlMovie.tt = tt
        urlMovie.displayType = user.getDisplayType(tt)   
        
        if imovie and imovie.plot:
            urlMovie.title = imovie.title
            urlMovie.iyear = imovie.iyear
            urlMovie.plot = imovie.plot.outline  
            urlMovie.poster = imovie.poster
            urlMovie.genres = imovie.getGenreList()
            
        else:
            result = self.getEndPoint('title/get-overview-details', tt)
            d = Dget(result)
        
            urlMovie.title = d.get('title', 'title')
            urlMovie.iyear = d.get('title', 'year')
            urlMovie.plot = d.get('plotOutline', 'text')
            urlMovie.poster = d.get('title', 'image', 'url') 
            urlMovie.genres = d.get('genres')
            
        return urlMovie
        
    def processFilm(self, user, film):
        poster = Poster()
                
        titleType = film.get('titleType', '')
        if titleType in excludes or 'year' not in film:
            return None
        
        if titleType not in ['movie', 'tvMovie' ]:
            info("Consider titleType '" + titleType + "'")
        
        tt = getID(film)
        
        #poster.addMoviePoster(tt, getImageUrl(film), None)
        
        urlMovie = UrlMovie()
        
        urlMovie.tt = tt
        urlMovie.title = film['title']
        urlMovie.iyear = film['year']         
        urlMovie.displayType = user.getDisplayType(tt)     
        urlMovie.poster = getImageUrl(film)    

        self.setMoviePersonsDb(urlMovie, tt)
        if len(urlMovie.actors) == 0 and 'principals' in film:
            for prin in film['principals']:
                urlPerson = UrlPerson()
                urlPerson.nm = prin['id']
                urlPerson.name = prin['name']
                urlMovie.actors.append(urlPerson)
                
        self.setPlotDb(urlMovie, tt)

        return urlMovie
    
    
    def setMoviePersonsDb(self, urlMovie, tt):
        
        personMovies = PersonMovie.query.filter(PersonMovie.tt == tt).order_by(PersonMovie.srt).all();
        
        for personMovie in personMovies:
            if personMovie.role == 'director':
                urlMovie.directors.append(personMovie.getUrlPerson())
            elif personMovie.role == 'writer':
                urlMovie.writers.append(personMovie.getUrlPerson())
            else:
                urlMovie.actors.append(personMovie.getUrlPerson())

                
    def setCrew(self, urlMovie, tt):
        timer = Timer()
        crew = self.getEndPoint('title/get-top-crew', tt)
        timer.elapse('Got crew for ' + tt)
        
        directors = crew.get('directors', [])
        urlMovie.directors = self.getMoviePersons(directors, tt, 'director')
        
        writers = crew.get('writers', [])
        urlMovie.writers = self.getMoviePersons(writers, tt, 'writer')
        info('Done crew for tt=' + tt)

    def setCast(self, urlMovie, tt):
        timer = Timer()
        actors = self.getEndPoint('title/get-top-cast', tt)
        #actors = ['/name/nm0252230/', '/name/nm0931324/', '/name/nm1055413/', '/name/nm0000093/', '/name/nm4833412/', '/name/nm6003176/', '/name/nm0061262/', '/name/nm1788122/', '/name/nm0779427/', '/name/nm4832920/', '/name/nm5244012/', '/name/nm1591232/', '/name/nm1058940/', '/name/nm0453115/', '/name/nm0077512/', '/name/nm0131966/', '/name/nm6003177/', '/name/nm1663252/', '/name/nm5164937/', '/name/nm1323822/', '/name/nm4977564/', '/name/nm0698354/', '/name/nm0531333/', '/name/nm3868449/', '/name/nm0341174/', '/name/nm0566279/', '/name/nm0114177/', '/name/nm0390259/', '/name/nm0825805/', '/name/nm0316079/', '/name/nm1733525/', '/name/nm1212722/', '/name/nm0896117/', '/name/nm4438871/', '/name/nm4206786/', '/name/nm0263625/', '/name/nm0200452/', '/name/nm0005299/', '/name/nm2143282/', '/name/nm1314193/', '/name/nm0878807/', '/name/nm2880343/', '/name/nm4000650/', '/name/nm3697867/', '/name/nm2958419/', '/name/nm3963894/', '/name/nm5123156/', '/name/nm0420228/', '/name/nm0005569/'] 
        timer.elapse('Got cast for ' + tt)
        
        urlMovie.actors = self.getMoviePersons(actors, tt, 'actor')   
        info('Done cast for tt=' + tt)
        
            
    def getMoviePersons(self, jlist, tt, role): 
        stmt = PersonMovie.__table__.delete().where(PersonMovie.tt == tt).where(PersonMovie.role == role)
        db.session.execute(stmt)
        db.session.commit()
        
        srt = 1
        rtn = []
        for j in jlist:
            nm = getID(j)
            if isinstance(j, str):
                job = ''
            else:
                job = j.get('job','')
                
            personUrl = self.processPerson(tt, nm, role, job, srt)

            rtn.append(personUrl)
            srt += 1
            
        return rtn
        

    
    def processPerson(self, tt, nm, role, job, srt):
        timer = Timer()
                             
        personMovie = PersonMovie(
            tt=tt, 
            nm=nm,
            role=role,
            job=job,
            srt=srt,
            src='rapid')

        try:
            db.session.add(personMovie)
            db.session.commit()

        except:
            db.session.rollback() 
            err = sys.exc_info()[1].orig.args[1]
            if 'Duplicate' in err:
                warn(err)
            else:
                error(err)
                raise Exception
            
        
        person = Person.query.filter(Person.nm == nm).first()
        if person == None or person.insert_time == None:
            j = self.getEndPoint('actors/get-bio', nm)
            if j != None:
                self.replacePerson(j)

               
            
        personMovie = PersonMovie.query.filter(PersonMovie.tt == tt,
                                               PersonMovie.nm == nm,
                                               PersonMovie.job == job,
                                               PersonMovie.role == role).first();
                                               
        if personMovie.person == None:
            warn('Person is none for tt=' + tt + ', nm=' + nm + ', role=' + role + ', job=' + job)
        else:
            timer.elapse(str(srt) + ' Processed ' + role + "(" + job + "): " + personMovie.person.name + '(' + nm + ')')
        
        return personMovie.getUrlPerson()
            
    def replacePerson(self, j): 
        #timer = Timer()
        nm = getID(j)
   
        stmt = Person.__table__.delete().where(Person.nm == nm)
        db.session.execute(stmt)
        db.session.commit()
        

        if 'image' in j:
            image_url = j['image']['url']
        else:
            image_url = ''
            
            
        person = Person(
            nm=nm, 
            name=j['name'],
            legacyNameText = j.get('legacyNameText', ''),
            birthDate = makeDate(j.get('birthDate', None)),
            birthPlace = j.get('birthPlace', ''),
            deathDate = makeDate(j.get('deathDate', None)),
            deathPlace = j.get('deathPlace', ''),
            deathCause = j.get('deathCause', ''),
            gender = j.get('gender', 'None'),
            height = j.get('heightCentimeters', 0),
            realName = j.get('realName', ''),
            image_url = image_url,
            insert_time = datetime.utcnow()
            )
        db.session.add(person)
        db.session.commit()
        
        #timer.elapse('Replaced ' + actor.name + '(' + actor.nm + ')' )
             
               
    def refreshAdder(self, tt, what):
        urlMovie = UrlMovie()
        if what == 'plot':
            self.setPlotEndpoint(urlMovie, tt)
            return urlMovie.plot
        elif what == 'cast':
            self.setCast(urlMovie, tt)
            return urlMovie.displayCast()  
        elif what == 'crew':
            self.setCrew(urlMovie, tt)
            return urlMovie.markCrew()
   
            
    def getGenreList(self):
        genres = Genre.query.filter(Genre.chart == 'T').order_by(Genre.srt).all()
        return genres
         
    def setPlotDb(self, urlMovie, tt):
        iplot = ImdbPlot.query.filter(ImdbPlot.tt == tt).first()
        
        if iplot != None:
            if iplot.outline != '':
                urlMovie.plot = iplot.outline
            else:
                urlMovie.plot = iplot.summary
                
                
    def setPlotEndpoint(self, urlMovie, tt):
        stmt = ImdbPlot.__table__.delete().where(ImdbPlot.tt == tt)
        db.session.execute(stmt)
        db.session.commit()
        
        dmovie = self.getEndPoint('title/get-overview-details', tt)
        #dmovie = {'id': '/title/tt0068646/', 'title': {'@type': 'imdb.api.title.title', 'id': '/title/tt0068646/', 'image': {'height': 1982, 'id': '/title/tt0068646/images/rm746868224', 'url': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg', 'width': 1396}, 'runningTimeInMinutes': 175, 'title': 'The Godfather', 'titleType': 'movie', 'year': 1972}, 'certificates': {'US': [{'certificate': 'R', 'certificateNumber': 23101, 'country': 'US'}]}, 'ratings': {'canRate': True, 'rating': 9.2, 'ratingCount': 1579080, 'topRank': 2}, 'genres': ['Crime', 'Drama'], 'releaseDate': '1972-03-24', 'plotOutline': {'author': 'Carl Schultz', 'id': '/title/tt0068646/plot/po1065441', 'text': '2 The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.'}, 'plotSummary': {'author': 'srijanarora-152-448595', 'id': '/title/tt0068646/plot/ps2220100', 'text': 'The Godfather "Don" Vito Corleone'}}
        summary = ''
        outline = ''
        
         
        if 'plotSummary' in dmovie:
            summary = dmovie['plotSummary']['text']
        if 'plotOutline' in dmovie:
            outline = dmovie['plotOutline']['text']


        iplot = ImdbPlot(tt=tt, summary=summary, outline=outline) 
        db.session.add(iplot)
        db.session.commit()

        self.setPlotDb(urlMovie, tt)


    def getFind(self, search):
        url = URL + 'title/find'
        q = {'q': search}
        r = requests.request("GET", url, headers=headers, params=q)
        j = r.json()
        results = j['results']
        return results
    
    def getPopularGenres(self):
        url = URL + 'title/list-popular-genres'
        r = requests.request("GET", url, headers=headers) 
        j = r.json()
        results = j['results']
        return results
        
    def getMoviesByGenre(self, genre):

        if genre == 'all':
            url = URL + 'title/get-most-popular-movies'
            q = {}

        else:
            url = URL + 'title/get-popular-movies-by-genre'
            q = {"genre":"/chart/popular/genre/" + genre}
            # These did not work for multiple genre
            #q = {'genre': '/chart/popular/genre/sci-fi,comedy,thriller,musical'}
            #q = {'genre': '/chart/popular/genre/sci-fi,/chart/popular/genre/comedy,/chart/popular/genre/thriller,/chart/popular/genre/musical'}
            #q = {'genre': ['/chart/popular/genre/sci-fi','/chart/popular/genre/comedy','/chart/popular/genre/thriller','/chart/popular/genre/musical']}

        r = requests.request("GET", url, headers=headers, params=q) 
        results = r.json()
        
        return results

    def getEndPoint(self, endPoint, id):
        url = URL + endPoint
        letter = id[0]
        const = letter + 'const'

        
        q = {const: id}
        r = requests.request("GET", url, headers=headers, params=q)
 
        try:
            j = r.json()
            return j
        except:
            warn('Could not get endPoint ' + endPoint + ' for ' + id + ', reason=' + r.text + " Retrying")

            time.sleep( 5 )

            r = requests.request("GET", url, headers=headers, params=q)
            j = r.json()
            return j


    
    
    '''
    def getOverviewDetails(self, tt):
        url = TITLE + "get-overview-details"
        #q = {"currentCountry":"US", "tconst": tt}
        q = {"tconst": tt}
        r = requests.request("GET", url, headers=headers, params=q)
        d = r.json()
        return d
        
    def getDetails(self, tt):
        url = TITLE + "get-details"
        q = {"tconst": tt}
        r = requests.request("GET", url, headers=headers, params=q)
        d = r.json()
        return d
        
        def getTopCast(self, tt, endpoint):
        timer = Timer()
        info('Getting top cast for ' + tt)
        

               

        casts = self.getEndPoint('title/get-top-cast', tt)
        srt = 1
        for cast in casts:
            self.processActor(tt, cast, srt)
            srt = srt + 1

        actors = PersonMovie.query.filter(PersonMovie.tt == PersonMovie.role == 'actor').order_by(PersonMovie.srt).all()    
        timer.elapse("Returning " + str(len(actors)) + ' top actors for ' + tt)
        
        return actors
        
        
        '''