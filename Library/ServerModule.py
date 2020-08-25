from app.models import User, UserMovie, UserColumn
from flask_login import current_user
from app import db
import datetime
import re
import logging

def processValue(value, dataType):
    if dataType in ['number', 'currency', 'comma']:
        return processNumber(value)
    elif dataType == "date":
        return processDate(value)
    else:
        return processText(value)


def processText(value):
    rtn = Rtn()
    rtn.value = value

    return rtn

def processNumber(value):
    rtn = Rtn()
    if value == "":
        rtn.value = "0"
    else:
        value = value.replace('$', '')
        value = value.replace(',', '')
        
        rtn.value = value 
        if value == '.':
            rtn.message = 'silent'
        else:
            try:
                float(value)
            except ValueError:
                rtn.message = "Please enter a number"

    return rtn
    
def processDate(value):
    rtn = Rtn()
    
    if value == "":
        rtn.value = "0000-00-00"
        return rtn
        
    try:
        date = datetime.datetime.strptime(value, '%m/%d/%Y')
        rtn.value = date.strftime("%Y-%m-%d")
    except ValueError:
        try:
            date = datetime.datetime.strptime(value, '%m/%d/%y')
            rtn.value = date.strftime("%Y-%m-%d")
        except ValueError:
            prog = re.compile("^[0-9/]+$")
            result = prog.match(value)
            if result == None:
                rtn.message = "Invalid Date.  Please use something like 10/6/2015"
            else:
                rtn.message = "silent"
                
    return rtn
                    
class Rtn:
    def __init__(self):
        self.value = ""
        self.message = ""
                            
class Inputter():
    def processInput(self, imdbMovieId, name, value, dataType):
        rtn = processValue(value, dataType)

        if rtn.message == '':
            column = getattr(UserMovie, name)
            UserMovie.query.filter_by(user_id = current_user.id, imdb_movie_id = imdbMovieId).update({column: rtn.value})
            db.session.commit()
            logging.getLogger('gk').info('Inputter.processInput: Updated UserMovie, user_id=' + str(current_user.id) + ', ' + name + '=' + rtn.value)
            return ""
        elif rtn.message == 'silent':
            return ""
        else:
            return rtn.message
        
    def processSettingsDisplayInput(self, user, name, colAttribute, dataType, value): 
        rtn = processValue(value, dataType)
        
        if rtn.message == '':
            column = getattr(UserColumn, colAttribute)
            UserColumn.query.filter(UserColumn.user_id == user.id, UserColumn.name == name).update({column: rtn.value})
            db.session.commit()
            logging.getLogger('gk').info('Inputter.processSettingsDisplayInput: Updated UserColumn, user_id=' + str(user.id) + ', ' + name + '.' + colAttribute + '=' + rtn.value)
            return ""
        elif rtn.message == 'silent':
            return ""
        else:
            return rtn.message

