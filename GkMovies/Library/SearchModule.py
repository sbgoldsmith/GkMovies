from Library.ConstantsModuleF import Constants
from Library.HelperModuleF import add0
#from wtforms.ext.django.fields import ModelSelectField

clearSearchValues = ['this', 'series', 'title', 'genre', 'actor', 'crew', 'plot_outline', 'plot_summary', 'my_date_seen', 'my_rating', 'my_review', 'dateAdded']
keyMap = {'outline':'plot_outline', 'summary':'plot_summary'}

class Searcher():
    def __init__(self):
        
        self.this = ''
        self.displayType = 'seen'
        
        self.series = ''
        self.seriesFirst = False
        self.title = ''
        self.genre = ''
        self.actor = ''
        self.crew = ''
        self.plot_outline = ''
        self.plot_summary = ''
        
        self.dateAdded = ''
        self.my_date_seen = ''
        self.my_rating = ''
        self.my_review = ''
        
        self.user01 = ''
        self.user02 = ''
        self.user03 = ''
        self.user04 = ''
        self.user05 = ''
        self.user06 = ''
        self.user07 = ''
        self.user08 = ''
        self.user09 = ''
        self.user10 = ''

        self.addTypeSelect = ''
        self.addTitle = ''
        self.addPerson = ''
        self.addLesser = ''
        
        self.reseted = False
        
    def setInit(self):
        i = 0

    def setArgs(self, args):           
        self.this = ''

        self.reseted = False 
        if 'displayType' in args:
            self.displayType = args['displayType']
            
        for key in args:
            if key.endswith('Search'):
                self.this = key.replace('Search', '').replace('plot.', 'plot_')
                value = args[key]
                value = value.replace("+", " ")
                
                setattr(self, self.this, value)


    def setArg(self, form):
        if 'displayType' in form:
            self.displayType = form['displayType']
            return 
        
        if 'elementName' not in form:
            return
        
        key = form['elementName']
        self.this = key.replace('Search', '').replace('plot.', 'plot_')
        value = form['elementValue'].replace("+", " ")
        setattr(self, self.this, value)
        
    def setDisplayType(self, args):
        if 'displayType' in args:
            self.displayType = args['displayType']
            
    def clearFilters(self):
        self.reseted = True
            
        clearAllValues = clearSearchValues + Constants().userColumns
        for value in clearAllValues:
            setattr(self, value, '')  
        
    def search(self, movies, column):
        name = keyMap.get(column.key, column.key)
        op = self.op(name)
        
        if not op:
            return movies

        if '%' in op:
            movies = movies.filter(column.like(op))
        else:
            movies = movies.filter(column.op('regexp')(op))

        return movies
    
    def getKeyValue(self, name):
        if name in keyMap:
            return keyMap[name]
        else:
            return name;
        
        
    def op(self, name):
        value = getattr(self, name)
        if value == '':
            return None
        
        if 'date' in name:
            value = self.getDateValue(value)
        else:
            value = "%" + value + "%"
    
        return value
    
    def getDateValue(self, value):  
        if value.startswith('/'):
            # looking for a year
            value = "^" + value[1:len(value)]
            
        elif value.endswith('/'):
            # looking for month and or date
            value = '%-' + value[0:len(value)-1] + '%'
        elif '/' in value:
            count = value.count('/')
            if count == 1:
                value = "%" + value.replace('/', '-') + "%"
            else:
                s1 = value.find('/')
                s2 = value.rfind('/')
                
                year = value[s2+1:len(value)]
                mo = int(value[0:s1])
                dy = int(value[s1+1:s2])

                value = year + '%' + add0(mo) + '-' + add0(dy) + '%'
        return value
                
    def hasSearch(self):
        anySearch = self.title + self.genre + self.actor + self.crew + self.plot_outline + self.plot_summary + self.dateAdded + self.my_date_seen + self.my_rating + self.my_review
        anySearch += self.user01 + self.user02 + self.user03 + self.user04 + self.user05 + self.user06 + self.user07 + self.user08 + self.user09 + self.user10
        return anySearch != ''
    
    def get(self, name):
        name = name.replace("plot.", "plot_")
        rtn = getattr(self, name)
        return rtn
        
    def isNew(self):
        rtn = self.this != '' or self.reseted
        return rtn
    
    def getThis(self):
        rtn = self.this.replace("plot_", "plot.")
        return rtn
    
    