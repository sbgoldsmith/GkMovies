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
    
    
steps_1_2 = [
    ['ALTER TABLE', 'imdb_movie', "ADD rottenTomatoes INT NOT NULL AFTER imdbVotes;"],
    ['ALTER TABLE', 'imdb_movie', "ADD metaCritic     INT NOT NULL AFTER rottenTomatoes;"],
           
    ['INSERT INTO', 'column_attribute', "VALUES (0, 'rottenTomatoes',  'center', 'top', 'T', 'F', 'F', 'F', 'int', 17);"], 
    ['INSERT INTO', 'column_attribute', "VALUES (0, 'metaCritic',      'center', 'top', 'T', 'F', 'F', 'F', 'int', 18);"], 
    ['UPDATE', 'column_attribute', "SET ordr = 19 where name = 'genre';"],
    ['UPDATE', 'column_attribute', "SET ordr = 20 where name = 'actor';"],                    
    ['UPDATE', 'column_attribute', "SET ordr = 21 where name = 'plot';"],         
    ['UPDATE', 'column_attribute', "SET ordr = 22 where name = 'deleteMovie';"],                                
            ]

usteps_1_2 = [                  
    ['INSERT INTO', 'user_column', "VALUES (0, {{user_id}}, 'rottenTomatoes', 'Rotten Toma.', 8, 1, 'percent', 'F', 21);"], 
    ['INSERT INTO', 'user_column', "VALUES (0, {{user_id}}, 'metaCritic',     'Meta Critic',  8, 1, 'number',  'F', 22);"],                               
            ]
        
        
steps_1_3 = [
    ['ALTER TABLE', 'user', "ADD user_since DATETIME AFTER admin;"],
    ['ALTER TABLE', 'user', "ADD as_login VARCHAR(32) NOT NULL AFTER admin;"],
    ['UPDATE', 'user', 'SET as_login = login;'],
    ['INSERT INTO', 'version', "VALUES ('4', '2020-09-15 20:45:38', '1.3', 'Add movies working spinner and results indication, more logging, fix skewed email', 'Ralph Knag');"], 
            ]

class UpdateSchema():
    def __init__(self):
        if os.name == 'nt':
            SQLALCHEMY_DATABASE_URI = "mysql://sbg:BABylon55!!@localhost/gkmovies"
        else:
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://sbg:BABylon55!!@localhost:3306/gkmovies'
        
        mysql_engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
        self.connection = mysql_engine.connect()
       

    def update(self):
        version = "1.3"
        steps = steps_1_3
        usteps = None

        c = self.connection
        trans = c.begin()

        try:
            if steps != None:
                for step in steps:
                    cmd = step[0] + " " + tbl(step[1]) + " " + step[2]
                    self.connection.execute(cmd)
            
            if usteps != None:    
                users = User.query.all()
                for user in users:
                    for ustep in usteps:
                        cmd = ustep[0] + " " + tbl(ustep[1]) + " " + ustep[2]
                        cmd = cmd.replace('{{user_id}}', str(user.id))
                        self.connection.execute(cmd)

            trans.commit()
            return "Version " + version + " Commands commited"
        except:
            trans.rollback()
            return "Error, Commands rolled back.\n" + str(sys.exc_info())
        
        