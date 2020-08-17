from Library.HelperModuleF import getTable, isImdb
from Library.HighlightModule import highlight
from Library.TimerModule import Timer
from Library.ConstantsModuleF import Constants
from flask import Markup
from app.models import UserColumn
from app import db

#.DEBUG move to Imdb or vs

def p(name, value):
    if value == None:
        return ""; 
    else:
        return " " + name + "=\"" + str(value) + "\""
    
def narg(args, strg):
    if strg in args:
        return args[strg]
    else:
        return ""

     
        
class FlaskHelper(Constants):       
    def setArgs(self,  user, args):
        self.user = user
        if args != None:
            self.args = args
            self.nargs = {}
            
            for searchColumn in self.searchColumns:
                sColumn = searchColumn + 'Search'
                self.nargs.update( {sColumn : narg(args, sColumn) } )
            
        stop = 1

            
    def getArgValue(self, thisSearch):
        rtn = self.nargs[thisSearch + 'Search']
        return rtn;
  
    def getArrow(self, thisCol):
        if self.user.order_by == thisCol:
            if self.user.order_dir == 'asc':
                return "/static/images/upArrow.jpg"
            else:
                return "/static/images/dnArrow.jpg"
        else:
            return "/static/images/upArrow.jpg"
        
     
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
        value = self.getValue(movie, col)
        
        if value == None:
            rtn = ""
        elif col.attribute.dataType == "comma":
            rtn = "{:,.0f}".format(float(value))
        elif col.attribute.dataType == "time":
            rtn = str(value)[1:5]
        elif col.attribute.dataType == "date":
            if value == '0000-00-00':
                rtn = ''
            else:
                rtn = '{d.month}/{d.day}/{d.year}'.format(d=value)

        elif col.attribute.dataType == "int":
            if value == 0:
                rtn = ""
            else:
                rtn = value
        elif col.attribute.searchable == 'T' and  col.attribute.editable == 'F':  
            sname = col.name + "Search"
            lookfor = self.nargs[sname]
            rtn = highlight(value, lookfor)

        else:
            rtn = value
        return rtn

    def getFormatString(self, strg, col):       
        sname = col.name + "Search"
        lookfor = self.nargs[sname]
        rtn = highlight(strg, lookfor)
        return rtn

    '''
    def getAreaCols(self, col):
        idx = col.attribute.inputCols.find(":")
        return col.attribute.inputCols[0:idx]
    
    def getAreaRows(self, col):
        idx = col.attribute.inputCols.find(":")
        return col.attribute.inputCols[idx+1]
    '''
   
    def strong(self, called, line, label):
        print ("called=" + called)
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
            UserColumn.width: dflt.width,
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
                UserColumn.width: dflt.width,
                UserColumn.vis: dflt.vis,
                UserColumn.srt: dflt.srt})

        db.session.commit()    
        
    def updateUser(self, form):
        print('in flasker first=' + form.firstName.data)
                
        self.user.login = form.login.data
        self.user.email = form.email.data    
        self.user.firstName = form.firstName.data 
        self.user.lastName = form.lastName.data
        
        if form.password.data != 'NothingToSee':
            self.user.set_password(form.password.data)
            
        db.session.commit()
            
            
            