from Library.DbModule import Dber
from Library.HighlightModule import highlight
from Library.LoggerModule import Timer, debug
from Library.ConstantsModuleF import Constants
from flask import request, Markup
from werkzeug.utils import secure_filename
from app.models import UserColumn
from app import db
from datetime import datetime
import math
import os
import requests
 
#.DEBUG move to Imdb or vs

def p(name, value):
    if value == None:
        return ""; 
    else:
        return " " + name + "=\"" + str(value) + "\""
      

class Flasker(Constants):
    def __init__(self):
        self.dber = Dber()
        
    def formatDate(self, value):
        if value == None:
            return ''
        
        if isinstance(value, str):
            if value == '0000-00-00' or value == '' or value == None:
                return ''
            else:   
                value = datetime.strptime(value, '%Y-%m-%d')
                
        rtn = '{d.month}/{d.day}/{d.year}'.format(d=value)
        return rtn
    
        
    def setArgs(self,  user, searcher):
        self.user = user
        if searcher != None:
            self.searcher = searcher

    
    def getArgValue(self, thisSearch):
        rtn = self.searcher.get(thisSearch)
        return rtn;
  
    def getArrow(self, thisCol):
        if self.user.order_by == thisCol:
            if self.user.order_dir == 'asc':
                return "/static/images/upArrowRed.png"
            else:
                return "/static/images/dnArrowRed.png"
        else:
            return "/static/images/upArrowRed.png"
        
     
    def getVisibility(self, thisCol):
        if self.user.order_by == thisCol:
            return "visible"
        else:
            return "hidden"
        
    def getValue(self, movie, col):    
        if self.dber.isImdb(col.name):
            if '.' in col.name:
                i = col.name.find('.')
                plotName = col.name[i+1:len(col.name)]
                value = getattr(movie.imdb_movie.plot, plotName)
            else:
                value = getattr(movie.imdb_movie, col.name)
        else:
            value = getattr(movie, col.name)
        
        return value
    
        
            
    def getSelected(self, col, value):
        if col.dataFormat == value:
            return "selected"
        else:
            return ""
    
    def getFormatValue(self, movie, col):
        #try:
            return self.tryFormatValue(movie, col)
        #except:
            #return "#ERR"


    def tryFormatValue(self, movie, col):
        value = self.getValue(movie, col)
        
        if col.attribute.searchable == 'T' and  col.attribute.editable == 'F':  
            lookfor = self.searcher.get(col.name)
            if col.dataFormat == 'date':
                value = self.formatDate(value)
            rtn = highlight(value, lookfor)
        else:
            rtn = self.formatValue(col.dataFormat, value)
            

        return rtn


    def formatValue(self, dataFormat, value):
        if value == None or value == '' or value == 0 or value == '0':
            rtn = ""
        elif dataFormat == "comma":
            rtn = "{:,.0f}".format(float(value))
        elif dataFormat == 'currency':
            rtn = '${:,.2f}'.format(float(value))
        elif dataFormat == "time":
            rtn = str(value)[1:5]
        elif dataFormat == "percent":
            rtn = str(value) + '%'
        elif dataFormat == "number":
            rtn = "{:.2f}".format(float(value))
            if rtn.endswith('0'):
                rtn = rtn[0:len(rtn)-1]
        elif dataFormat == 'integer':
            rtn = '{:d}'.format(int(value))
        elif dataFormat == "date":
                rtn = self.formatDate(value)
        else:
            rtn = value
        return rtn


    def getFormatString(self, strg, col):       
        lookfor = self.searcher.get(col.name)
        rtn = highlight(strg, lookfor)
        return rtn

   
    def strong(self, called, line, label):
        if called == line:
            return Markup("<strong>" + label + "</strong>")
        else:
            return label
    
    def plus(self, item):
        return item.replace(' ', '+')
            
    def isVisible(self, col):
        if col.vis == 'T':
            return 'checked'
        else:
            return ''

    def upCol(self, cuser, colName):
        col = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).first()
        
        if col.srt == 1:
            return
        
        srt = col.srt
        upcol = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.displayType == self.searcher.displayType, UserColumn.srt == srt - 1).first()

        col.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).update({UserColumn.srt: srt - 1})
        upcol.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == upcol.name, UserColumn.displayType == self.searcher.displayType).update({UserColumn.srt: srt})
        db.session.commit()

    def dnCol(self, cuser, colName):
        col = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.displayType == self.searcher.displayType, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).first()

        srt = col.srt
        dncol = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.displayType == self.searcher.displayType, UserColumn.srt == srt + 1).first()
        if dncol == None:
            return
       
        col.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).update({UserColumn.srt: srt + 1})
        dncol.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == dncol.name, UserColumn.displayType == self.searcher.displayType).update({UserColumn.srt: srt})
        db.session.commit()
        
        
    def resetCol(self, cuser, colName):
        dflt = UserColumn.query.filter(UserColumn.user_type == 'user', UserColumn.user_id == 1, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).first()
        col = UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).first()

        col.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == colName, UserColumn.displayType == self.searcher.displayType).update({
            UserColumn.label: dflt.label,
            UserColumn.cols: dflt.cols,
            UserColumn.rows: dflt.rows,
            UserColumn.vis: dflt.vis,
            UserColumn.dataFormat: dflt.dataFormat
            })

        db.session.commit()
        
    def resetSort(self, cuser):   
        dfltColumns = UserColumn.query.filter(UserColumn.user_type == 'user', UserColumn.user_id == 1, UserColumn.displayType == self.searcher.displayType).order_by(UserColumn.srt).all()
        for dflt in dfltColumns:
            UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.name == dflt.name, UserColumn.displayType == self.searcher.displayType).update({UserColumn.srt: dflt.srt})

        db.session.commit()    
        
    def resetAll(self, cuser):   
        dfltColumns = UserColumn.query.filter(UserColumn.user_type == 'user', UserColumn.user_id == 1, UserColumn.displayType == self.searcher.displayType).order_by(UserColumn.srt).all()
        for dflt in dfltColumns:
            UserColumn.query.filter(UserColumn.user_type == cuser.user_type, UserColumn.user_id == cuser.user_id, UserColumn.user_id == self.user.id, UserColumn.name == dflt.name, UserColumn.displayType == self.searcher.displayType).update({
                UserColumn.label: dflt.label,
                UserColumn.cols: dflt.cols,
                UserColumn.rows: dflt.rows,
                UserColumn.vis: dflt.vis,
                UserColumn.dataFormat: dflt.dataFormat,
                UserColumn.srt: dflt.srt})

        db.session.commit()    
        
    def updateUser(self, form):   
        self.user.login = form.login.data
        self.user.email = form.email.data    
        self.user.firstName = form.firstName.data 
        self.user.lastName = form.lastName.data
        self.user.city = form.city.data
        self.user.state = form.stateSelect.data
        self.user.country = form.countrySelect.data
        
        f = form.face.data
        
        filename = secure_filename(f.filename)

        if filename != '':
            f.save(os.path.join(self.facePath, filename))
            self.user.face = filename
        
        if form.password.data != 'NothingToSee':
            self.user.set_password(form.password.data)
            
        db.session.commit()
            
    def quote(self, strg):
        return strg.replace("'", "\\'")
    
    def getButtonClass(self, thisType, typeSelect):
        if thisType == typeSelect:
            return "button_down"
        else:
            return "button_up"
    
    def getButtonColor(self, thisType, typeSelect):
        if thisType == typeSelect:
            return "color:red;"
        else:
            return ""
            
    def getPersonImageWidth(self, movies):
        if len(movies) == 0:
            return 50
        else:
            return 80
        
    def getPersonNameSize(self, movies):
        if len(movies) == 0:
            return ''
        else:
            return Markup("style='font-size: 18px;'")
        
    def isChecked(self, strg):
        if strg == 'true':
            return ' checked '
        else:
            return ''
            
    def nav(self, location, label):
        if request.url_rule and request.url_rule.rule.startswith(location):
            return Markup("<strong>" + label + "</strong>")
        else:
            return Markup(label)
        
    def getMoviesFound(self, numMovies):
        if numMovies == 0:
            return "No Movies Found"
        elif numMovies == 1:
            return "1 Movie Found"
        else:
            return str(numMovies) + " Movies Found"
    