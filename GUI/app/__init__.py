#Author: Yicheng Jin
#Date: 12/28/2021
import os

from flask import Flask # import Flask lib
from flask_navigation import Navigation
from flask_session import Session


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap

# from prototype.config import Config
from config import Config

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.config.from_object(Config)

# navigation bar items
nav = Navigation(app)
nav.Bar('side', [
    # nav.Item('Login','login'),
    nav.Item('About pyChip', 'about'),
    nav.Item('Few Shot Algorithm', 'form'),
    nav.Item('LSTM Algorithm','lstm'),
    nav.Item('Learning History','history')
])

# file paths
app.config['UPLOAD_PATH'] = 'protected'
app.config['SECRET_KEY'] = 'any secret string'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = os.path.join('static', 'username')
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)#DATABASE
migrate = Migrate(app, db)#MIGRATE
Session(app)

from app import routes, models