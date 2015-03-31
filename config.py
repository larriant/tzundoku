import os
basedir =os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'tzundoku.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

