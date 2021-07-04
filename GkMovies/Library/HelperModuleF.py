from datetime import date, datetime
from functools import reduce
from Library.BeanModule import Rtn
import re
   
        
class Dget():
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
    def get(self, *keys):
        rtn = reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys, self.dictionary)
        if rtn == None:
            return ''
        else:
            return rtn
        
    def getInt(self, *keys):
        rtn = reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys, self.dictionary)
        if rtn == None:
            return 0
        else:
            return rtn

    
    def getFloat(self, *keys):
        rtn = reduce(lambda d, key: d.get(key, None) if isinstance(d, dict) else None, keys, self.dictionary)
        if rtn == None:
            return 0.0
        else:
            return rtn


class Process():
    def value(self, value, dataFormat):
        if dataFormat in ['number', 'currency', 'integer', 'comma']:
            return self.number(value)
        elif dataFormat == "date":
            return self.date(value)
        else:
            return self.text(value)
    
    
    def text(self, value):
        rtn = Rtn()
        rtn.value = value
    
        return rtn
    
    def number(self, value):
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
    
    def date(self, value):
        rtn = Rtn()
        
        if value == "":
            rtn.value = "0000-00-00"
            return rtn
            
        try:
            date = datetime.strptime(value, '%m/%d/%Y')
            rtn.value = date.strftime("%Y-%m-%d")
        except ValueError:
            try:
                date = datetime.strptime(value, '%m/%d/%y')
                rtn.value = date.strftime("%Y-%m-%d")
            except ValueError:
                prog = re.compile("^[0-9/]+$")
                result = prog.match(value)
                if result == None:
                    rtn.message = "Invalid Date.  Please use something like 10/6/2015"
                else:
                    rtn.message = "silent"
                    
        return rtn


def getImageUrl(dmovie):
    if 'image' in dmovie:
        return dmovie['image']['url']
    elif 'Poster' in dmovie:
        return dmovie['Poster']
    else:
        return ''
    
def add0(intg):
    if intg < 10:
        return "0" + str(intg)
    else:
        return str(intg)
 

def nn(strg):
    if strg == None:
        return ""
    else:
        return strg
    

def getItemList(commas):
    rtn = []
    commas += ","
    index = commas.find(",")

    start = 0;
    while index > -1:
        item = commas[start:index].strip()
        rtn.append(item)
         
        start = index + 1
        index = commas.find(",", start, len(commas))
         
    return rtn;



def makeDate(strg):
    if isinstance(strg, date):
        strg = str(strg)
        
    if strg == None or strg == '':
        return '0000-00-00'
    
    elif len(strg) == 4:
        #
        # Year only
        #
        return strg + "-01-01"
    elif len(strg) == 7:
        return strg + "-01"
    else:
        return strg

def formatDate(value):
    if  isinstance(value, date):
        rtn = '{d.month}/{d.day}/{d.year}'.format(d=value)
    else:
        rtn = ''
    return rtn

def formatFloat(value):
    if value == 0:
        rtn = ''
    else:
        rtn = str(value)
    return rtn


def tf(btf):
    if btf:
        return 'T'
    else:
        return 'F'
    
def isTf(tf):
    return tf == 'T'
