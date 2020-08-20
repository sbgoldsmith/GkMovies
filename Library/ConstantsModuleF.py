import os

class Constants:
    
    if os.name == 'nt':
        posterPath = "D:/GkMovies/GkMovies/app/static/posters/"
    else:
        posterPath = "/var/www/html/GkMovies/app/static/posters/"
        
    
    userColumns = ['seen', 'stars', 'review', 'user01', 'user02', 'user03', 'user04', 'user05' ]
    
    def __init__(self):
        self.searchColumns = ["title", "review", "genre", "actor", "plot", "user01", "user02", "user03", "user04", "user05"]
        self.userColumns = ['seen', 'stars', 'review', 'user01', 'user02', 'user03', 'user04', 'user05' ]
        self.widthFactor = 8
        
        
        