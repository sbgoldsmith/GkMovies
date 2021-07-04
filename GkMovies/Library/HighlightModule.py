from enum import Enum
from flask import Markup
from Library.HelperModuleF import nn

#
#Highlight functions
#
fontStart = "<font color=\"red\" style=\"BACKGROUND-COLOR:#FFFF00\">"
fontEnd = "</font>"
    
    
class Range(Enum):
    TEXT = 1
    HTML = 2
    DONE = 3
    
    
def highlight(strg, lookfor):
    lookfor = nn(lookfor)
    if lookfor == "":
        return strg 

    rtn = ""    

    i = 0;
    tup = (Range.TEXT, "")
     
    while i < len(strg):
        tup = nextRange(i, strg)
        if tup[0] == Range.HTML:
            rtn += tup[1]
        else:
            #loop
            rtn += buildFonting(tup[1], lookfor)
         
        i += len(tup[1])   

         
    return Markup(rtn)

def buildFonting(strg, lookfor): 
    strg = nn(strg)
    lookfor = nn(lookfor)
    
    rtn = ""
    oldIndex = 0
    looki = strg.lower().find(lookfor.lower(), oldIndex)
    
    while looki > -1:
        before = strg[oldIndex:looki]
        segment = strg[looki:looki+len(lookfor)]
        rtn += before + fontStart + segment + fontEnd
        
        oldIndex = looki + len(lookfor)
        looki = strg.lower().find(lookfor.lower(), oldIndex)
    
    rtn += strg[oldIndex:len(strg)]
    return rtn

def nextRange(start, strg):
    if  start == len(strg):
        tup = (Range.DONE, "")
    else:
        sstart  = strg[start:start+1]
        if sstart == "<":
            end = strg.find(">", start)
            tup = (Range.HTML, strg[start:end+1])
        else:
            end = strg.find("<", start)
            if end == -1: end = len(strg)
            tup = (Range.TEXT, strg[start:end])
    
    return tup
    