import os
basedir =os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://tzundoku:tablet30@localhost/tzundoku'

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

