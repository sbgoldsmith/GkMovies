import os 
import urllib
from Library.LoggerModule import info, debug
from Library.ConstantsModuleF import Constants

class Poster(Constants):
    def addMoviePoster(self, tt, url, imovie):
        
        rtn = 0;
        imagePath = self.posterPath + tt + ".jpg"
        debug('Checking tt= ' + tt + ' for download, imagePath = ' + imagePath)
        
        if imovie != None:
            imovie.poster = url
            
        if os.path.exists(imagePath):
            debug('Checking tt= ' + tt + ' path exists')
            valid = 'T'
         
        elif url == "N/A" or url == '':
            debug('Checking tt= ' + tt + ', url=' + url)
            valid = 'F'
        
        else: 
            try:
                info('Downloading to ' + imagePath)
                urllib.request.urlretrieve(url, imagePath)
                valid = 'T'
                rtn = 1
            except:
                error('Could not Download ' + str(url))
                valid = 'F'
              
        if imovie != None:
            imovie.poster_valid = valid
            
        return rtn  
    
    