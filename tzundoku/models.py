import datetime
from flask.ext.login import current_user, login_required

from tzundoku import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    pwdhash = db.Column(db.String(120))
    moderator = db.Column(db.Boolean, default= True)
    admin = db.Column(db.Boolean, default = True)
    posts = db.relationship('Post', backref='users')
    items = db.relationship('Item', backref='users')
    dokus = db.relationship('Doku', backref='users')
    postvotes = db.relationship('Postvote', backref='users')
    itemvotes = db.relationship('Itemvote', backref='users')
    dokuvotes = db.relationship('Dokuvote', backref='users')

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

doku_item = db.Table('doku_item', 
    db.Column('doku_id', db.Integer, db.ForeignKey('dokus.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)

children = db.Table('children',
    db.Column('child_id', db.Integer, db.ForeignKey('dokus.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('dokus.id'))
    )
    
class Doku(db.Model):
    __tablename__ = 'dokus'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), unique= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp =  db.Column(db.DateTime, default=datetime.datetime.utcnow)
    items = db.relationship('Item', secondary=doku_item, backref=db.backref('dokus'))
    parents = db.relationship('Doku', secondary=children, primaryjoin="Doku.id == children.c.child_id", secondaryjoin="Doku.id == children.c.parent_id", backref=db.backref('children'))
    itemvotes = db.relationship('Itemvote', backref='dokus')
    dokuvotes = db.relationship('Dokuvote', backref='dokus')

    def __init__(self, title, user_id=None, timestamp=None):
        self.title = title
        self.user_id = user_id 
        self.timestamp = timestamp 

    def __repr__(self):
        return '<Doku %r>' % (self.title)

    def delete(self):
        doku = Doku.query.filter_by(id = self.id).first()
        db.session.delete(doku)
        db.session.commit()

    def showitems(self):
        showitems = []
        for a in self.items:
            showitems.append(a)
        showitems.sort(key=lambda x: x.numvotes(self.id), reverse=True)
        return showitems
    
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(30))
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    composer = db.Column(db.String(50))
    creator = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    year = db.Column(db.Integer)
    link = db.Column(db.String(50))
    imglink = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts = db.relationship('Post', backref='items')
    itemvotes = db.relationship('Itemvote', backref='items')


    def __repr__(self):
        return '<Item %r>' % (self.title)
    
    def __init__(self, type, title, artist, year, link, imglink, user_id, timestamp):
        self.type = type
        self.title= title 
        self.artist = artist
        self.year = year
        self.link = link
        self.imglink = imglink
        self.user_id= user_id 
        self.timestamp = timestamp 
 
    def delete(self):
        item = Item.query.filter_by(id = self.id).first()
        db.session.delete(item)
        db.session.commit()

    def numvotes(self, doku_id):
        upvotes = Itemvote.query.filter_by(item_id=self.id).filter_by(doku_id=doku_id).filter_by(vote = True).count()
        downvotes = Itemvote.query.filter_by(item_id=self.id).filter_by(doku_id=doku_id).filter_by(vote = False).count() 
        return upvotes - downvotes

    def showposts(self):
        showposts= []
        for a in self.posts:
            showposts.append(a)
        showposts.sort(key=lambda x: x.numvotes(), reverse=True)
        return showposts


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    postvotes = db.relationship('Postvote', backref='posts')

    def __repr__(self):
        return '<Post %r>' % (self.message) 

    def __init__(self,user_id, message, timestamp, item_id):
        self.user_id = user_id 
        self.message = message
        self.timestamp = timestamp 
        self.item_id = item_id 

    def delete(self):
        post = Post.query.filter_by(id = self.id).first()
        for a in post.postvotes:
            db.session.delete(a)
        db.session.delete(post)
        db.session.commit()        

    def numvotes(self):
        upvotes = Postvote.query.filter_by(post_id=self.id).filter_by(vote = True).count()
        downvotes = Postvote.query.filter_by(post_id=self.id).filter_by(vote = False).count() 
        return upvotes - downvotes 
      
class Postvote(db.Model):
    __tablename__='postvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))     
    vote = db.Column(db.Boolean) #True is upvote, False is downvote
    
    def __init__(self, user_id , post_id,  vote):
        self.user_id = user_id 
        self.post_id = post_id 
        self.vote = vote

class Itemvote(db.Model):
    __tablename__='itemvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    doku_id = db.Column(db.Integer, db.ForeignKey('dokus.id'))
    vote = db.Column(db.Boolean) #True is upvote, False is downvote

    def __init__(self, user_id, item_id, doku_id, vote):
        self.user_id = user_id
        self.item_id = item_id
        self.doku_id = doku_id
        self.vote = vote 

class Dokuvote(db.Model):
    __tablename__='dokuvotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doku_id = db.Column(db.Integer, db.ForeignKey('dokus.id'))     
    vote = db.Column(db.Boolean) #True is upvote, False is downvote
    
    def __init__(self, user_id , doku_id,  vote):
        self.user_id = user_id 
        self.doku_id = doku_id 
        self.vote = vote


