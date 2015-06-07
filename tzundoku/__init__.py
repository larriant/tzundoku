import os
from jinja2 import nodes
from jinja2.ext import Environment, loopcontrols

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.restful import Api

tzundoku = Flask(__name__)
tzundoku.config.from_object('config')

db = SQLAlchemy(tzundoku)

lm = LoginManager()
lm.init_app(tzundoku)

tzundoku_api=Api(tzundoku)

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])

from tzundoku import views, models, api

lm.login_view = 'login'


