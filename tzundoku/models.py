from tzundoku import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(64), index = True, unique=True)
    pwdhash = db.Column(db.String(120), index=True)
    moderator = db.Column(db.Boolean, default= True)
    admin = db.Column(db.Boolean, default = True)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def make_admin(self):
        user = User.query.filter_by(id = User.id).first()
        user.admin = True
        db.session.commit()

    def make_moderator(self):
        user= User.query.filter_by(id = User.id).first()
        user.moderator = True
        db.session.commit()

    def is_admin(self):
        user = User.query.filter_by(id = User.id).first()
        if user.admin == True:
            return True
        else:
            return False
        
    def is_moderator(self):
        user = User.query.filter_by(id = User.id).first()
        if user.moderator == True:
            return True
        else:
            return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)
    
class Doku(db.Model):
    __tablename__ = 'dokus'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), index = True, unique= True)
    parent = db.Column(db.String(30), index = True, default="Top")
    added_by = db.Column(db.Integer, index = True, default= 1)
    timestamp =  db.Column(db.DateTime)

    def __init__(self, title, parent, added_by, timestamp):
        self.title = title
        self.parent = parent
        self.added_by = added_by
        self.timestamp = timestamp 

    def __repr__(self):
        return '<Doku %r>' % (self.title)

    def removedoku(self):
        doku = Doku.query.filter_by(id = self.id).first()
        db.session.delete(doku)
        db.session.commit()
        
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(30), index = True)
    title = db.Column(db.String(50), index = True)
    author = db.Column(db.String(50), index = True)
    composer = db.Column(db.String(50), index = True)
    creator = db.Column(db.String(50), index = True)
    artist = db.Column(db.String(50), index = True)
    year = db.Column(db.Integer, index = True)
    link = db.Column(db.String(50), index = True)
    added_by = db.Column(db.Integer, index = True, default= 1)
    timestamp = db.Column(db.DateTime)
    doku_id = db.Column(db.Integer, index = True)
    upvotes = db.Column(db.Integer, index = True, default = 0)
    downvotes = db.Column(db.Integer, index = True, default = 0)

    def __repr__(self):
        return '<Item %r>' % (self.title)
    
    def __init__(self, type, title, artist, year, link, added_by, timestamp, doku_id):
        self.type = type
        self.title= title 
        self.artist = artist
        self.year = year
        self.link = link
        self.added_by = added_by
        self.timestamp = timestamp 
        self.doku_id = doku_id

    def upvoteitem(self):
        item = Item.query.filter_by(id = self.id).first()
        item.upvotes += 1
        db.session.commit()

    def downvoteitem(self):
        item = Item.query.filter_by(id = self.id).first()
        item.downvotes += 1
        db.session.commit()


    def removeitem(self):
        item = Item.query.filter_by(id = self.id).first()
        db.session.delete(item)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    added_by = db.Column(db.Integer, index = True, default = 1)
    message = db.Column(db.String(500), index = True)
    timestamp = db.Column(db.DateTime)
    item_id = db.Column(db.Integer, index=True)
    upvotes = db.Column(db.Integer, index = True, default = 0)
    downvotes =  db.Column(db.Integer, index = True, default = 0)

    def __repr__(self):
        return '<Post %r>' % (self.message) 

    def __init__(self,added_by, message, timestamp, item_id):
        self.added_by = added_by
        self.message = message
        self.timestamp = timestamp 
        self.item_id = item_id

    def getusername(self):
        user = User.query.filter_by(id = self.added_by).first()
        return user.username
    
    def getitemtitle(self):
        item = Item.query.filter_by(id = self.item_id).first()
        return item.title

    def removepost(self):
        post = Post.query.filter_by(id = self.id).first()
        db.session.delete(post)
        db.session.commit()
    
    def upvotepost(self):
        post = Post.query.filter_by(id = self.id).first()
        post.upvotes += 1
        db.session.commit()

    def downvotepost(self):
        post = Post.query.filter_by(id = self.id).first()
        post.downvotes += 1
        db.session.commit()        
 
