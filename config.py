import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sajyd6w487349phofnjkshdf45698t74htfi'
    #SQLALCHEMY_DATABASE_URI = "mysql://sbg:BABylon55!!@localhost/gkmovies"
    SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://sbg:BABylon55!!@localhost/gkmovies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'steven.bl.goldsmith@gmail.com'
    MAIL_PASSWORD = 'Tgh2BCFneC8Z'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ADMINS = ['sgoldsmith@goldkeys.com']

    '''
    MAIL_SERVER = "smtp.goldkeys.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "sgoldsmith@goldkeys.com"
    MAIL_PASSWORD = "DEEP+email12"
    ADMINS = ['sgoldsmith@goldkeys.com']
    '''