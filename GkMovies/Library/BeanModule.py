from Library.ConstantsModuleF import Constants
from app.models import load_club, ImdbMovie, UserMovie
from flask import Markup
from flask_login import current_user

class Cuser(Constants):
    def __init__(self, user_type, user_id):
        self.user_type = user_type
        self.user_id = user_id
        if user_type == 'club':
            self.club = load_club(user_id)
            
    # Needed when called from session
    def setInit(self):
        if self.user_type == 'club':
            self.club = load_club(self.user_id)
            
    def __str__(self):
        return 'user_type=' + self.user_type + ', userId=' + str(self.user_id)

    def isClub(self):
        return self.user_type == 'club'
    
    def isClubNone(self):
        return self.user_type == 'club' and self.user_id == 0
    
    def isClubSome(self):
        return self.user_type == 'club' and self.user_id != 0
    
    def isClubOwner(self, current_user_id):
        return self.user_type == 'club' and self.club != None and current_user_id == self.club.owner_id
    
    def isLogin(self):
        return not current_user.is_anonymous
    
    def isUser(self):
        return  self.user_type == 'user' and self.user_id != 0
     
    def getAddWantTitle(self):
        if self.user_type == 'user':
            return Markup("I <U>Want</U><br>to see<br>this movie")
        else:
            return Markup(self.club.name + " Watch List")
        
    def getAddSeenTitle(self):
        if self.user_type == 'user':
            return Markup("I <U>Saw</U><br>this movie")
        else:
            return Markup(self.club.name + " Saw Movie")
        
    def getDisplayWantTitle(self):
        if self.user_type == 'user':
            return Markup("Movies I<br>Want to See")
        else:
            return Markup("Movies We<br>Want to See")
        
    def getDisplaySeenTitle(self):
        if self.user_type == 'user':
            return Markup("Movies I<br>Have Seen")
        else:
            return Markup("Movies We<br>Have Seen")
        
    def getDisplayType(self, tt):
        im = ImdbMovie.query.filter(ImdbMovie.tt == tt).first()
        if im == None:
            return None
        
        um = UserMovie.query.filter(UserMovie.user_type == self.user_type, UserMovie.user_id == self.user_id, UserMovie.imdb_movie_id == im.id).first()   
        if um:
            return um.displayType
        else:
            return None
        
        
    def addAllowedSeen(self, user_id):
        return self.user_type == 'user' or user_id == self.club.owner_id or self.club.allow_add_seen == 'T'
    
    def addAllowedWant(self, user_id):
        return self.user_type == 'user' or user_id == self.club.owner_id or self.club.allow_add_want == 'T'
    
    

            

class Rtn:
    def __init__(self):
        self.value = ""
        self.message = ""
        self.club = None
        
        
        