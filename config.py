import os

basedir =os.path.abspath(os.path.dirname(__file__))

if os.environ.get("TZUNDOKU_LOCAL") is not None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://tzundoku:tablet30@localhost/tzundoku'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
