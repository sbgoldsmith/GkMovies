from datetime import date
from functools import reduce

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

