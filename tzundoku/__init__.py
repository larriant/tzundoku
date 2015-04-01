import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


tzundoku = Flask(__name__)

tzundoku.config.from_object('config')

db = SQLAlchemy(tzundoku)

from tzundoku import views, models




