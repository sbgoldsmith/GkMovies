from Library.HelperModuleF import getTable, isImdb
from Library.HighlightModule import highlight
from Library.TimerModule import Timer
from Library.ConstantsModuleF import Constants
from flask import Markup
from app.models import UserColumn
from app import db
from datetime import datetime
import math

#.DEBUG move to Imdb or vs

def p(name, value):
    if value == None:
        return ""; 
    else:
        return " " + name + "=\"" + str(value) + "\""
      
        
class FlaskHelper(Constants):       
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
        if isImdb(col.name):
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
        try:
            return self.tryFormatValue(movie, col)
        except:
            return "#ERR"
        
        
    def tryFormatValue(self, movie, col):
        value = self.getValue(movie, col)
        
        if value == None or value == '':
            rtn = ""
        elif col.dataFormat == "comma":
            rtn = "{:,.0f}".format(float(value))
        elif col.dataFormat == 'currency':
            rtn = '${:,.2f}'.format(float(value))
        elif col.dataFormat == "time":
            rtn = str(value)[1:5]
        elif col.dataFormat == "date":
            if value == '0000-00-00' or value == '':
                rtn = ''
            else:
                date_object = datetime.strptime(value, '%Y-%m-%d')
                rtn = '{d.month}/{d.day}/{d.year}'.format(d=date_object)
        elif col.attribute.searchable == 'T' and  col.attribute.editable == 'F':  
            lookfor = self.searcher.get(col.name)
            rtn = highlight(value, lookfor)

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
        
    def isVisible(self, col):
        if col.vis == 'T':
            return 'checked'
        else:
            return ''

    def upCol(self, colName):
        col = UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == colName).first()
        
        if col.srt == 1:
            return
        
        srt = col.srt
        upcol = UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.srt == srt - 1).first()
        
       
        col.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == colName).update({UserColumn.srt: srt - 1})
        upcol.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == upcol.name).update({UserColumn.srt: srt})
        db.session.commit()

    def dnCol(self, colName):
        col = UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == colName).first()

        srt = col.srt
        dncol = UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.srt == srt + 1).first()
        if dncol == None:
            return
       
        col.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == colName).update({UserColumn.srt: srt + 1})
        dncol.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == dncol.name).update({UserColumn.srt: srt})
        db.session.commit()
        
        
    def resetCol(self, colName):
        dflt = UserColumn.query.filter(UserColumn.user_id == 1, UserColumn.name == colName).first()
        col = UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == colName).first()

        col.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == colName).update({
            UserColumn.label: dflt.label,
            UserColumn.cols: dflt.cols,
            UserColumn.rows: dflt.rows,
            UserColumn.vis: dflt.vis
            })

        db.session.commit()
        
    def resetSort(self):   
        dfltColumns = UserColumn.query.filter(UserColumn.user_id == 1).order_by(UserColumn.srt).all()
        for dflt in dfltColumns:
            UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == dflt.name).update({UserColumn.srt: dflt.srt})

        db.session.commit()    
        
    def resetAll(self):   
        dfltColumns = UserColumn.query.filter(UserColumn.user_id == 1).order_by(UserColumn.srt).all()
        for dflt in dfltColumns:
            UserColumn.query.filter(UserColumn.user_id == self.user.id, UserColumn.name == dflt.name).update({
                UserColumn.label: dflt.label,
                UserColumn.cols: dflt.cols,
                UserColumn.rows: dflt.rows,
                UserColumn.vis: dflt.vis,
                UserColumn.srt: dflt.srt})

        db.session.commit()    
        
    def updateUser(self, form):                
        self.user.login = form.login.data
        self.user.email = form.email.data    
        self.user.firstName = form.firstName.data 
        self.user.lastName = form.lastName.data
        
        if form.password.data != 'NothingToSee':
            self.user.set_password(form.password.data)
            
        db.session.commit()
            
            
            