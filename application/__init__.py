import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

app.secret_key = 'secret'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'application.db')

db = SQLAlchemy(app)

from application import views, models
