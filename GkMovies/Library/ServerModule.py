from app.models import User, UserMovie, UserColumn, ClubCache
from flask_login import current_user
from app import db
from datetime import datetime
from Library.BeanModule import Rtn
from Library.LoggerModule import debug
from Library.HelperModuleF import Process

  
class Inputter():
    def processInput(self, cuser, imdbMovieId, name, value, dataFormat):
        process = Process()
        rtn = process.value(value, dataFormat)

        if rtn.message == '':
            column = getattr(UserMovie, name)
              
            userMovie  = UserMovie.query.filter(UserMovie.user_type == cuser.user_type, UserMovie.user_id == cuser.user_id, UserMovie.imdb_movie_id == imdbMovieId)
            userMovie.update({column: rtn.value})  
            db.session.commit()

            debug('Inputter.processInput: Updated UserMovie, user_id=' + str(current_user.id) + ', ' + name + '=' + rtn.value)
            return ""
        elif rtn.message == 'silent':
            return ""
        else:
            return rtn.message
        
        
                    

        
    def processSettingsDisplayInput(self, cuser, name, displayType, colAttribute, dataFormat, value): 
        process = Process()
        rtn = process.value(value, dataFormat)
        
        if rtn.message == '':
            column = getattr(UserColumn, colAttribute)
            UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == name, UserColumn.displayType == displayType).update({column: rtn.value})
            db.session.commit()
            debug('Inputter.processSettingsDisplayInput: Updated UserColumn, user_id=' + str(cuser.user_id) + ', ' + name + '.' + colAttribute + '=' + rtn.value)
            return ""
        elif rtn.message == 'silent':
            return ""
        else:
            return rtn.message












