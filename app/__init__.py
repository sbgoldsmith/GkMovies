from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Mail, Message

import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'index'
mail = Mail(app)
logging.addLevelName(15, 'TIMER')
logging.basicConfig(level=logging.DEBUG, format='gkm %(asctime)s %(levelname)s %(module)s line %(lineno)d %(message)s')
#
# Initialize Error Mail Handler
#  
class MySMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
 
        Format the record and send it to the specified addressees.
        """
        try:
            print("Starting MySMTPHandler")
            import smtplib
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
                

            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            print("Starting smtplib.SMTP_SSL")
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            #string.join(self.toaddrs, ","),
                            self.toaddrs[0],
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.login(self.username, self.password)
            print("Starting smtp.sendmail")
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
            
logger = logging.getLogger()

mail_handler = MySMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']), 
                             app.config['MAIL_USERNAME'], 
                             app.config['ADMINS'],
                             'Goldkeys Movies Error', 
                             (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))


mail_handler.setLevel(logging.ERROR)
logger.addHandler(mail_handler)


from app import routes, models, errors

'''
from app.models import User
from Library.AdderModuleF import Adder
from flask_login import current_user, login_user

user = User.query.filter_by(login = 'sbg').first()
adder = Adder()
message = adder.addMovie('tt2488496')


args = {'sortButton':'title', 'titleSearch': 'Star Wars',  'reviewSearch': '', 'genreSearch': '', 'actorSearch':'', 'plotSearch':'',\
        'user01Search':'', 'user02Search':'', 'user03Search':'', 'user04Search':'', 'user05Search':'', \
        'user06Search':'', 'user07Search':'', 'user08Search':'', 'user09Search':'', 'user10Search':''}
user = User.query.filter_by(login = 'sbg').first() 

imdb = ImdbFind()
imdb.displayMovies(user, args)
stop = 1

user = User.query.filter_by(login = 'sbg').first()
imdbFind = ImdbFind()
imdbFind.findMovies(user, 'Star Wars')

             

    
#---------------------+


from app.models import User, UserColumn, ImdbMovie
from app.Imdb import ImdbFind





from datetime import datetime
from Library.AdderModuleF import Adder
from Library.FlaskModule import FlaskHelper
from Library.ServerModule import Inputter
from sqlalchemy.orm import selectinload, joinedload, query
from app.email import send_email, send_password_reset_email




        
        


user.admin = 'T'
db.session.commit()








movies = imdbFind.displayMovies(user, args) 
 
for movie in movies:
    
    for actor in movie.imdb_movie.actor_movies:
        print('nm=' + actor.nm)
        print("actor=" + actor.actor.actor)

            


column = UserColumn.query.filter(UserColumn.user_id == 4, UserColumn.name == 'imdbVotes').all();
cols = UserColumn.query.filter(User.login == 'tara', UserColumn.name == 'user02').first();
for col in cols:
    if col.name == 'user02':
        print(col.dataFormat)


stop = 1
    

flasker = FlaskHelper()
flasker.setArgs(user, None)
flasker.resetSort()





inputter = Inputter()
message = inputter.processSettingsDisplayInput(user, 'poster', 'label', 'Hello')



user = User.query.filter_by(login = 'tara').first() 
imdbFind = ImdbFind()
imdbFind.deleteMovie(user, 939)


adder = Adder()
message = imdbFind.updateMovies(1, 20)
#imovie = ImdbMovie.query.filter_by(tt = 'tt0081109').first()
#adder.updateImdbMovie(imovie)




flasker = FlaskHelper()
flasker.setArgs(user, args)
for movie in movies:
    
    for actor in movie.imdb_movie.actor_movies:
        print('nm=' + actor.nm)
        print("actor=" + actor.actor.actor)

            
            
    for col in user.columns:
        rtn = flasker.getCell(col, movie)




'''