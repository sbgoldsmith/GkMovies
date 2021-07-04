from Library.ConstantsModuleF import Constants
from Library.HelperModuleF import getItemList
from app.models import Person, PersonMovie
from app import db

import urllib
import os 
import requests

class Actorer(Constants):
    def __init__(self):
        x = 1
        
    def findActor(self, actorName):
        http = "http://www.imdb.com/find?q="
        actorName = actorName.replace(" ", "+")
    
        #
        # First see if it is an exact match - these are the best.
        #
        nm = self.lookInPage(http + actorName + "&s=nm&exact=true")
        if len(nm) > 0: return nm
  
        #
        # Name not found.  Try removing foreign alt characters
        #
        nm = self.lookInPage(http + self.removeAlt(actorName) + "&s=nm&exact=true")
        if len(nm) > 0: return nm

        #
        # Still nothing.  Remove exact match and return first value in list
        #
        nm = self.lookInPage(http + self.removeAlt(actorName) + "&s=nm")
        if len(nm) > 0: return nm
    
        #
        # Damn, we're not doing well.  Just look anywhere
        #
        nm = self.lookInPage(http + self.removeAlt(actorName))
        if len(nm) > 0: return nm
    
        #
        # A Default when all else fails
        #
        nm = self.removeAlt(actorName)
        
    def lookInPage(self, q):
        look = "/name/nm"
        page = requests.get(url = q)
        content = str(page.content)
        
        loc = content.find(look)
        if loc > 0:
            rtn = content[loc+6:loc+15]
        else:
            rtn = ""
            
        return rtn

    def removeAlt(self, strg):
        return strg;
    
    
        