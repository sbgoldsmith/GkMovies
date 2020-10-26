import sqlalchemy
import sys
from sqlalchemy import create_engine
from app.models import User, ImdbMovie, ImdbPlot, UserColumn
import os
import requests
from app import db
from Library.AdderModuleF import Adder
from Library.DbModule import Dber
from Library.LoggerModule import info

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

class UpdateRelease():

    def update(self, version, step):
        info('UpdateRelease called, version=' + version + ', step=' + step)
        if version == '1.4':
            return self.update_1_4(step)

    def update_1_4(self, step):
        if step == '1':
            return self.manageUserColumns_1_4()
        elif step == '2':
            return self.initMovies_1_4()

     
    def manageUserColumns_1_4(self):
        dflt = User.query.filter(User.login == 'dflt').first()
        users = User.query.filter(User.login == 'sbg').order_by(User.lastName).order_by(User.firstName).all()
        
        for user in users:
            for displayType in ['seen', 'want']:
                dcols = dflt.getColumns(displayType)
                for dcol in dcols:
                    ucol = UserColumn.query.filter(UserColumn.user_id == user.id, UserColumn.name == dcol.name, UserColumn.displayType == displayType).first()
                    if ucol:
                        ucol.srt = dcol.srt
                        if ucol.name == 'user01':
                            ucol.label = 'User 01'
                            ucol.vis = 'F'
                        elif ucol.name == 'user02':
                            ucol.label = 'User 02'
                            ucol.vis = 'F'
                        elif ucol.name == 'user03':
                            ucol.label = 'User 03'
                            ucol.vis = 'F'
                    else:                        
                        newUCol = UserColumn(
                            user_id = user.id,
                            name=dcol.name,
                            label=dcol.label,
                            displayType=dcol.displayType,
                            cols=dcol.cols,
                            rows=dcol.rows,
                            dataFormat=dcol.dataFormat,
                            vis=dcol.vis,
                            srt=dcol.srt)
                        db.session.add(newUCol)


                        
                        
                    
        db.session.commit()                
        

        
        return 'Done Step 2 ManageUserColumns'
        
    def initMovies_1_4(self):
        adder = Adder()
        sql = '''select user_id, title, tt from user_movie um
left join imdb_movie im
on um.imdb_movie_id = im.id
where update_date is null
order by user_id desc, iyear desc, title; '''
        
        db = Dber();
        conn = db.getConnection()
        rs = conn.execute(sql)
        cnt = 0
        for row in rs:
            imovie = ImdbMovie.query.filter(ImdbMovie.tt == row['tt']).first()
            if not imovie.update_date:
                adder.updateImdbMovie(imovie, True, True)
                cnt += 1
                if cnt >= 20:
                    break
                
        return 'Updated ' + str(cnt) + ' movies'
    
    

    def updateSchema(self, version, step):
        version = "1.3"
        steps = steps_1_3
        usteps = None

        dber = Dber()
        dber.makeConnection()
        conn = dber.getConnection()
        trans = conn.begin()

        try:
            if steps != None:
                for step in steps:
                    cmd = step[0] + " " + tbl(step[1]) + " " + step[2]
                    conn.execute(cmd)
            
            if usteps != None:    
                users = User.query.all()
                for user in users:
                    for ustep in usteps:
                        cmd = ustep[0] + " " + tbl(ustep[1]) + " " + ustep[2]
                        cmd = cmd.replace('{{user_id}}', str(user.id))
                        conn.execute(cmd)

            trans.commit()
            return "Version " + version + " Commands commited"
        except:
            trans.rollback()
            return "Error, Commands rolled back.\n" + str(sys.exc_info())
        
                