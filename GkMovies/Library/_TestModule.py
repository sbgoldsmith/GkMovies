from app.models import User, UserMovie, UserColumn, ImdbMovie, Club, ClubUser, ClubUserMovie
from app.forms import ContactForm, getStateChoices
from datetime import datetime, date
from flask import jsonify
from Library.UpdateReleaseModule import UpdateRelease
from Library.AdderModuleF import Adder
from Library.OmdbModule import Omdb
from Library.PagerModule import Pager
from Library.SearchModule import Searcher
from Library.DisplayModule import Display
from Library.ContactModule import Contacter
from Library.AdminModule import Adminer
from Library.FlaskModule import Flasker
from Library.RapidModule import Rapid
from Library.DbModule import Dber
from Library.LoggerModule import Timer
from Library.HelperModuleF import Process, formatDate
from Library.ClubberModule import Clubber
from Library.BeanModule import Cuser
from Library.ServerModule import Inputter
import os

version = '1.3'
titles = {'home':'Home Page', 'addMovies':'Add to My Movies', 'displayMovies':'Display My Movies', 'settings':'Settings', 'contact':'Contact Us'}
jsons = {'pager': 'Pager', 'searcher': 'Searcher'}
args = {'reset_search': '', 'sortButton':'title', 'displayType':'seen', \
        'titleSearch': '',  'reviewSearch': '', 'genreSearch': '', 'actorSearch':'', 'plot.outlineSearch':'', 'plot.summarySearch':'',\
        'my_date_seenSearch':'', 'my_ratingSearch':'', 'my_reviewSearch':'', \
        'user01Search':'', 'user02Search':'', 'user03Search':'', 'user04Search':'', 'user05Search':'', \
        'user06Search':'', 'user07Search':'', 'user08Search':'', 'user09Search':'', 'user10Search':''}

def test():
    if os.name != 'nt':
        return 
    
    user = User.query.filter_by(login = 'sbg').first()
    
    cuser = Cuser('user', 2)
    searcher = Searcher()
    display = Display()
    movies = display.displayMovies(user, cuser, searcher, 'title')
    for movie in movies:
        print(movie.imdb_movie.title)
        for clubUserMovie in movie.clubUserMovies:
            print('    ' + clubUserMovie.club.name)
    stop = 1
   
'''
    
    clubber = Clubber()
    rtn = clubber.getCache(48, 1177)
    json = jsonify(rtn)
    
    cuser = Cuser('user', 30)
    clubUserMovies = ClubUserMovie.query.filter(ClubUserMovie.club_id == 48, UserMovie.imdb_movie_id == 1390, UserMovie.user_type == 'user')\
        .join(UserMovie)\
        .join(User)\
        .order_by(User.lastName)\
        .all()
    

    for clubUserMovie in clubUserMovies:
        userMovie = clubUserMovie.userMovie
        print (userMovie.user.firstName + ' ' + userMovie.user.lastName + ' ' + str(userMovie.my_date_seen))
    

  
    clubber = Clubber()
    clubber.makeVerticalDivide(cuser, current_user)
    
    displayType = 'want'
    tt = 'tt8463714'
    adder = Adder()
    response = adder.addMovie(cuser, displayType, tt )
       
    if cuser.user_type == 'club':
        clubber = Clubber()
        clubber.addMovie(cuser, displayType, tt)

            
            
            
    omdb = Omdb()
    movies = omdb.find(cuser, 'tt8463714')
    
    single_message = adder.updateSingleImdbMovie('tt8463714', True, True)
    
    imovie = ImdbMovie.query.filter_by(tt = 'tt8463714').first()    
    adder.updateImdbMovie(imovie, False, False, False)


    rapid = Rapid()
    movies = rapid.listMovies(current_user, 'book')
    
    cuser = Cuser('user', 28)
    clubber = Clubber()
    clubber.setClubMovie(cuser, 2, current_user, 339)

    total = 55
    cnt = 3
    
    avg = float(total) / float(cnt)
    savg = "{:.2f}".format(float(total) / float(cnt))
            
    clubber = Clubber()
    clubber.setClubMovie(7, 1228)
    clubber.getMembersMovie(current_user, 1228)
    
    rapid = Rapid()
    movies = rapid.listMovies(current_user, 'book')
    for movie in movies:
        print(movie.tt)
  
    for clubUser in current_user.clubs:
        print(clubUser.club.name)
         
    stop = 1
       
    club =  Club.query.filter(Club.club_id == 7).first()
    for clubUser in club.clubUsers:
        print('name=' + clubUser.user.lastName)
        
    rapid = Rapid()
    names = rapid.getGenreNamesFromCodes('none')

    rapid.listMoviesByGenreRankPopularity(user, 'rank', True, 'horror,sci_fi')
    
    adder = Adder()
    imovie = ImdbMovie.query.filter(ImdbMovie.tt == 'tt6723592').first()
    result = adder.updatePopularImdbMovie()
    #result = adder.updateRankImdbMovie()
    #result = adder.noRankDups()
     
    rapid = Rapid()
    movies = rapid.listPersonMovies(user, 'nm0000434')
    
    ur = UpdateRelease()
    ur.update_1_5('2')
    
    searcher = Searcher()
    #searcher.setArg({'elementName':'actorSearch', 'elementValue':'hanks'})
    searcher.setArg({'elementName':'crewSearch', 'elementValue':'Penny Marshall'})
    
    

    
    
    rapid = Rapid()
    film = rapid.getEndPoint('title/get-meta-data', 'tt6155172')
    
    adder = Adder()
    #single_message = adder.updateSingleImdbMovie('tt0468569', False, False)
    
    rank_message = adder.updateRankImdbMovie(10)
    

    movies = rapid.listMoviesByGenre(user, 'action', 'rank')
    

    
    adder = Adder()
    response = adder.addImdbMovie('tt5697572')
    
    ur = UpdateRelease()
    ur.initMovies_1_4_1()

    movies = rapid.listMoviesByGenre(user, 'mystery')
 

    #genres = rapid.getGenreList()
    movies = rapid.listMoviesByGenre(user, 'comedy')


    
    

    
    user = User.query.filter_by(login = 't1').first()


     
    user = User.query.filter_by(login = 't1').first()
    searcher = Searcher()
    searcher.setArgs(args)
    display = Display()
    movies = display.displayMovies(user, searcher, 'title')
    flasker = Flasker()
    
    for movie in movies:
        for col in user.getColumns('want'):
            rtn = flasker.getFormatValue(movie, col)
            print(col.name + '=' + str(rtn))
           
    us = UpdateRelease()
    message = us.update('1.4', '2')
    print(message)

    flasker = Flasker()
    col = UserColumn.query.filter(UserColumn.user_id == 1, UserColumn.name == 'my_date_seen').first()
    flasker.getFormatValue(movies[0], col)
                           
                           
    stop = 1  
    
    
    adminer = Adminer()
    message = adminer.deleteUser('t4', False)
    print(message)
             
    choices = []
    
    users = User.query.order_by(User.lastName).order_by(User.firstName).all()
    for user in users:
        name = user.firstName + ' ' + user.lastName + ' (' + user.login + ")"
        choice = (user.login, name)
        choices.append(choice)   
        

    
    args2 = {'clear_search' : 'T'}
    
    searcher = Searcher()
    searcher.setArgs(args) 
    searcher.setArgs(args2) 
    
    

    
 user = User.query.filter_by(login = 'sbg').first()

 
     
    adder = Adder()
    oldest_message = adder.updateOldestImdbMovies(2, False, True)


import requests
surl = "http://www.omdbapi.com/?apikey=4bcae80b&type=movie&s=" + str.replace('10', " ", "+")
r = requests.get(url = surl) 

        
        




from app.models import User
from Library.DisplayModule import Display
user = User.query.filter_by(login = 't1').first()
columns = user.getColumns('seen')
for col in columns:
    print('name=' + col.name + ', align=' + col.attribute.align)
    




display = Display()
display.seen(user, 'tt0050083')

 


from app.models import UrlMovie
from Library.RapidModule import Rapid
rapid = Rapid()
urlMovie = UrlMovie()
rapid.setCast(urlMovie, 'tt0448115')
stop = 1




      
from Library.AdderModuleF import Adder
adder = Adder()
message = adder.addMovie('tt0448115', 'seen')





from app.models import ImdbMovie
imovie = ImdbMovie.query.filter_by(tt = 'tt0068646').first()
actors = imovie.getActors(5)



   


flasker = Flasker()
flasker.setArgs(user, args)

for personMovie in movies[0].imdb_movie.person_movies:
    if personMovie.role != 'actor':
        continue
    
    print(personMovie.person.nm + " " + personMovie.person.name )




from Library.RapidModule import Rapid
 

user = User.query.filter_by(login = 'sbg').first()
for col in user.columns:
    print(col.name + ", " + col.attribute.align)




imovie = ImdbMovie.query.filter_by(tt = 'tt0068646').first()
print(imovie.plot.outline)
print(imovie.plot.summary)

     
rapid = Rapid()
rapid.refreshAdder('tt0068646', 'plot')









from app.models import User, Person, UrlMovie, PersonMovie
from Library.OmdbModule import Omdb

from Library.LoggerModule import Timer
from Library.HelperModuleF import getPersonDateRange


#rapid = Rapid()
person = Person.query.filter(Person.nm == 'nm0000003').first()
f = getPersonDateRange(person)



#person = rapid.listPerson('nm0000005')








film = rapid.getEndPoint('title/get-details', 'tt2527338')

#film = {'@type': 'imdb.api.title.title', 'id': '/title/tt0076759/', 'image': {'height': 2827, 'id': '/title/tt0076759/images/rm3263717120', 'url': 'https://m.media-amazon.com/images/M/MV5BNzVlY2MwMjktM2E4OS00Y2Y3LWE3ZjctYzhkZGM3YzA1ZWM2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg', 'width': 1820}, 'runningTimeInMinutes': 121, 'title': 'Star Wars: Episode IV - A New Hope', 'titleType': 'movie', 'year': 1977}
rapid.processFilm(user, film, 0)
timer.elapse('All done')



   
   


user = User.query.filter_by(login = 'sbg').first() 
rapid = Rapid()
movie = rapid.getEndPoint('actors/get-all-filmography', 'nm0219136')
 
stop = 1







   
   




import requests

url = "https://imdb8.p.rapidapi.com/title/get-plots"

querystring = {"tconst":"tt0031381"}

headers = {
    'x-rapidapi-host': "imdb8.p.rapidapi.com",
    'x-rapidapi-key': "0079b1e126msh9e9ad2ba4a5bee7p1d8b00jsn472b69b29949"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
stop = True   


from app.models import Version
lastest = Version.query.order_by(Version.install_date).first()
d = lastest.getFormatInstallDate()


from app.models import User
from Library.AdderModuleF import Adder
from flask_login import current_user, login_user

user = User.query.filter_by(login = 'sbg').first()
adder = Adder()
message = adder.addMovie('tt6723592')






from Library.PagerModule import Pager
page = Pager()

if hasattr(pager, 'setArgs'):
    print('T')
else:
    print('F')
    

from Library.SearchModule import Searcher
args = {'reset_search': 'T', 'sortButton':'title', 'titleSearch': 'men',  'reviewSearch': '', 'genreSearch': '', 'actorSearch':'', 'plotSearch':'',\
        'my_date_seen':'', 'my_rating':'', 'my_review':'', \
        'user01Search':'', 'user02Search':'', 'user03Search':'', 'user04Search':'', 'user05Search':'', \
        'user06Search':'', 'user07Search':'', 'user08Search':'', 'user09Search':'', 'user10Search':''}



searcher = Searcher()
searcher.setArgs(args)




from collections import namedtuple
from Library.PagerModule import Pager
import json
import jsonpickle
from json import JSONEncoder

args = {'pageSelected':4}
session = {}


pager.setArgs(args, 930)    
session['pager'] = jsonpickle.encode(pager)
       
        
pager = Pager()
j = json.dumps(pager.toJson())
j2 = json.loads(j)

j3 = jsonpickle.encode(pager)
#pager = json.loads(j2, object_hook=pagerDecoder)
pager = jsonpickle.decode(j3)


print(pager.getNumPages())
stop = 1;





    



    


def getPageRange(page, per_page, total):
    start = (page - 1) * per_page
    end = start + per_page
    return range(start, end)
    
r = getPageRange(1, 10, 900)







from app.models import User, UserColumn, ImdbMovie
from app.Imdb import ImdbFind





from datetime import datetime
from Library.AdderModuleF import Adder
from Library.FlaskModule import Flasker
from Library.ServerModule import Inputter
from sqlalchemy.orm import selectinload, joinedload, query
from app.email import send_email, send_password_reset_email




        
        


user.admin = 'T'
db.session.commit()


 
for movie in movies:
    
    for actor in movie.imdb_movie.actor_movies:
        print('nm=' + actor.nm)
        print("actor=" + actor.actor.actor)

            


column = UserColumn.query.filter(UserColumn.user_id == 4, UserColumn.name == 'imdbVotes').all();
cols = UserColumn.query.filter(User.login == 'tara', UserColumn.name == 'user02').first();
for col in cols:
    if col.name == 'user02':
        print(col.dataFormat)




inputter = Inputter()
message = inputter.processSettingsDisplayInput(user, 'poster', 'label', 'Hello')



user = User.query.filter_by(login = 'tara').first() 
imdbFind = ImdbFind()
imdbFind.deleteMovie(user, 939)







flasker = Flasker()
flasker.setArgs(user, args)
for movie in movies:
    
    for actor in movie.imdb_movie.actor_movies:
        print('nm=' + actor.nm)
        print("actor=" + actor.actor.actor)

            
            





'''