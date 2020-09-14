import sqlalchemy
import sys
from sqlalchemy import create_engine
from app.models import User
import os

def tbl(table):
    if os.name == 'nt':
        table = 'zts_' + table
        return table
    else:
        return table
    
    
class UpdateSchema():
    def __init__(self):
        if os.name == 'nt':
            SQLALCHEMY_DATABASE_URI = "mysql://sbg:BABylon55!!@localhost/gkmovies"
        else:
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://sbg:BABylon55!!@localhost:3306/gkmovies'
        
        mysql_engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
        self.connection = mysql_engine.connect()
       
        
        
        
    def update_1_2(self):
        steps = [
                    ['ALTER TABLE', 'imdb_movie', "ADD rottenTomatoes INT NOT NULL AFTER imdbVotes;"],
                    ['ALTER TABLE', 'imdb_movie', "ADD metaCritic     INT NOT NULL AFTER rottenTomatoes;"],
                   
                    ['INSERT INTO', 'column_attribute', "VALUES (0, 'rottenTomatoes',  'center', 'top', 'T', 'F', 'F', 'F', 'int', 17);"], 
                    ['INSERT INTO', 'column_attribute', "VALUES (0, 'metaCritic',      'center', 'top', 'T', 'F', 'F', 'F', 'int', 18);"], 
                    ['UPDATE', 'column_attribute', "SET ordr = 19 where name = 'genre';"],
                    ['UPDATE', 'column_attribute', "SET ordr = 20 where name = 'actor';"],                    
                    ['UPDATE', 'column_attribute', "SET ordr = 21 where name = 'plot';"],         
                    ['UPDATE', 'column_attribute', "SET ordr = 22 where name = 'deleteMovie';"],                                
                ]
        
        usteps = [                  
                    ['INSERT INTO', 'user_column', "VALUES (0, {{user_id}}, 'rottenTomatoes', 'Rotten Toma.', 8, 1, 'percent', 'F', 21);"], 
                    ['INSERT INTO', 'user_column', "VALUES (0, {{user_id}}, 'metaCritic',     'Meta Critic',  8, 1, 'number',  'F', 22);"],                               
                ]
                
        c = self.connection
        trans = c.begin()

        try:
            for step in steps:
                cmd = step[0] + " " + tbl(step[1]) + " " + step[2]
                self.connection.execute(cmd)
                
            users = User.query.all()
            for user in users:
                for ustep in usteps:
                    cmd = ustep[0] + " " + tbl(ustep[1]) + " " + ustep[2]
                    cmd = cmd.replace('{{user_id}}', str(user.id))
                    self.connection.execute(cmd)
                
                
          
            trans.commit()
            return "Commands commited"
        except:
            trans.rollback()
            return "Error, Commands rolled back.\n" + str(sys.exc_info())


