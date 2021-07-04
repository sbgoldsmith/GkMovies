from Library.ConstantsModuleF import Constants
from app.models import UserMovie, ImdbMovie
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Dber():
    def __init__(self):
        constants = Constants()
        self.allUserColumns = constants.userColumns + constants.myColumns
        
    def makeConnection(self):
        if os.name == 'nt':
            SQLALCHEMY_DATABASE_URI = "mysql://sbg:BABylon55!!@localhost/gkmovies"
        else:
            SQLALCHEMY_DATABASE_URI='mysql+pymysql://sbg:BABylon55!!@localhost:3306/gkmovies'
        
        self.mysql_engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
        self.connection = self.mysql_engine.connect()
        
    def getConnection(self):
        self.makeConnection()
        return self.connection
    
    def getTable(self, colName):
        if colName in self.allUserColumns:
            table = UserMovie
        else:
            table = ImdbMovie
            
        return table
    
    def isImdb(self, colName):
        rtn = not colName in self.allUserColumns
        return rtn



    