import os 
import urllib
from Library.LoggerModule import info
from Library.ConstantsModuleF import Constants

class Poster(Constants):
    def addMoviePoster(self, tt, url, imovie):
        rtn = 0;
        imagePath = self.posterPath + tt + ".jpg"
        if imovie != None:
            imovie.poster = url
            
        if os.path.exists(imagePath):
            valid = 'T'
         
        elif url == "N/A" or url == '':
            valid = 'F'
        
        else: 
            try:
                info('Downloading to ' + imagePath)
                urllib.request.urlretrieve(url, imagePath)
                valid = 'T'
                rtn = 1
            except:
                info('Could not download ' + url)
                valid = 'F'
              
        if imovie != None:
            imovie.poster_valid = valid
            
        return rtn  
    
    