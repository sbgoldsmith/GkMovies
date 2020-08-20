import os

class Constants:
    
    if os.name == 'nt':
        posterPath = "D:/GkMovies/GkMovies/app/static/posters/"
    else:
        posterPath = "/var/www/html/GkMovies/app/static/posters/"
        
    
     
    def __init__(self):
        self.searchColumns = ["title", "genre", "actor", "plot", "user01", "user02", "user03", "user04", "user05", 'user06', 'user07', 'user08', 'user09', 'user10' ]
        self.userColumns = ['user01', 'user02', 'user03', 'user04', 'user05', 'user06', 'user07', 'user08', 'user09', 'user10' ]
        self.widthFactor = 8
        
        
        