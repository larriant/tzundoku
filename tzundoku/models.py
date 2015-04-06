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
    
class Doku(db.Model):
    __tablename__ = 'dokus'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), unique= True)
    parent = db.Column(db.String(30), default="Top")
    user_id = db.Column(db.Integer, default= 1)
    timestamp =  db.Column(db.DateTime)
    items = db.relationship('Item', secondary=doku_item, backref=db.backref('dokus'))

    def __init__(self, title, parent, user_id, timestamp):
        self.title = title
        self.parent = parent
        self.user_id = user_id 
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
    type = db.Column(db.String(30))
    title = db.Column(db.String(50))
    author = db.Column(db.String(50))
    composer = db.Column(db.String(50))
    creator = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    year = db.Column(db.Integer)
    link = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posts = db.relationship('Post', backref='items')

    def __repr__(self):
        return '<Item %r>' % (self.title)
    
    def __init__(self, type, title, artist, year, link, user_id, timestamp):
        self.type = type
        self.title= title 
        self.artist = artist
        self.year = year
        self.link = link
        self.user_id= user_id 
        self.timestamp = timestamp 

    def upvoteitem(self):
        item = Item.query.filter_by(id = self.id).first()
        Itemvote(1, self.id, True)
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
    message = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    
    def __repr__(self):
        return '<Post %r>' % (self.message) 

    def __init__(self,user_id, message, timestamp, item_id):
        self.user_id = user_id 
        self.message = message
        self.timestamp = timestamp 
        self.item_id = item_id 

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
 

class Itemvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, default=1)
    item_id = db.Column(db.Integer, index=True)     
    vote = db.Column(db.Boolean, default=False) #True is upvote, False is downvote

    def __init__(self, added_by, item_id , vote):
        self.user_id = user_id 
        self.item_id = item_id
        self.vote = vote
    
