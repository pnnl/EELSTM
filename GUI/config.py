import os
basedir = os.path.abspath(os.path.dirname(__file__)) #get the abs route of current .py file




class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'

    #config the sql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_RUI') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 3

    #config the language
    LANGUAGES = ['en']
