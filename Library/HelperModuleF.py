from enum import Enum
from Library.ConstantsModuleF import Constants
from app.models import UserMovie, ImdbMovie
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

def getTable(colName):
    if colName in Constants().userColumns:
        table = UserMovie
    else:
        table = ImdbMovie
        
    return table

def isImdb(colName):
    return not colName in Constants().userColumns