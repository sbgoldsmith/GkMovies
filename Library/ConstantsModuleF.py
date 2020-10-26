import os

class Constants:
    
    if os.name == 'nt':
        posterPath = "D:/GkMovies/GkMovies/app/static/posters/"
        facePath = "D:/GkMovies/GkMovies/app/static/faces/"
    else:
        posterPath = "/var/www/html/GkMovies/app/static/posters/"
        facePath =  "/var/www/html/GkMovies/app/static/faces/"
    
     
    def __init__(self):
        self.searchColumns = ["title", "my_date_seen", "my_rating", "my_review", "genre", "actor", "plot", "user01", "user02", "user03", "user04", "user05", 'user06', 'user07', 'user08', 'user09', 'user10' ]
        self.myColumns = ["my_date_seen", "my_rating", "my_review"]
        self.userColumns = ['user01', 'user02', 'user03', 'user04', 'user05', 'user06', 'user07', 'user08', 'user09', 'user10' ]
        self.widthFactor = 8
        self.heightFactor = 15
        
        if os.name == 'nt':
            posterPath = "D:/GkMovies/GkMovies/app/static/posters/"
            facePath = "D:/GkMovies/GkMovies/app/static/faces/"
        else:
            posterPath = "/var/www/html/GkMovies/app/static/posters/"
            facePath =  "/var/www/html/GkMovies/app/static/faces/"
        
        
        