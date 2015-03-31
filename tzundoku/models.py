from tzundoku import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(64), index = True, unique=True)
    pwdhash = db.Column(db.String(120), index=True)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.set_password(password)


    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3 

    def __repr__(self):
        return '<User %r>' % (self.username)


class Doku(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), index = True, unique= True)
    parent = db.Column(db.String(30), index = True, default="Top")

    def __repr__(self):
        return '<Doku %r>' % (self.title)


