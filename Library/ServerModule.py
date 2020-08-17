from app.models import User, UserMovie, UserColumn
from flask_login import current_user
from app import db
import datetime
import re

def processValue(value, dataType):
    if dataType == "int":
        return processInt(value)
    elif dataType == "date":
        return processDate(value)
    else:
        return processText(value)


def processText(value):
    rtn = Rtn()
    rtn.value = value

    return rtn

def processInt(value):
    rtn = Rtn()
    if value == "":
        rtn.value = "0"
    elif not value.isdigit():
        rtn.value = value
        rtn.message = "Please enter a number"
    else:
        rtn.value = value
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
        print('processInput, dataType=' + dataType)
        rtn = processValue(value, dataType)
        print('processInput, rtn.message=' + rtn.message)
        if rtn.message == '':
            column = getattr(UserMovie, name)
            UserMovie.query.filter_by(user_id = current_user.id, imdb_movie_id = imdbMovieId).update({column: rtn.value})
            db.session.commit()
            print("Updated UserMovie, user_id=" + str(current_user.id) + ", " + name + "=" + rtn.value)
            return ""
        elif rtn.message == 'silent':
            return ""
        else:
            return rtn.message
        
    def processSettingsDisplayInput(self, user, name, colAttribute, dataType, value): 
        print("dataType=" + dataType)
        rtn = processValue(value, dataType)
        print(rtn.__dict__)
        
        if rtn.message == '':
            column = getattr(UserColumn, colAttribute)
            UserColumn.query.filter(UserColumn.user_id == user.id, UserColumn.name == name).update({column: rtn.value})
            db.session.commit()
            print("Updated UserColumn, user_id=" + str(user.id) + ", " + name + "." + colAttribute + "=" + rtn.value)
            return ""
        elif rtn.message == 'silent':
            return ""
        else:
            return rtn.message

