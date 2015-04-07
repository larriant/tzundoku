from flask import render_template, request, redirect, url_for, flash, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from tzundoku import tzundoku, db, lm
from .forms import LoginForm, RegistrationForm, AddDokuForm, AddItemForm, AddPostForm, UpvoteForm, DownvoteForm
from .models import User, Doku, Item, Post

import datetime
import legal

@lm.user_loader
def load_user(id):
    return User.query.get(id)

@tzundoku.route('/')
@tzundoku.route('/index')
def index():
    return render_template('index.html') 

@tzundoku.route("/login", methods=['GET', 'POST'])
def login(): 
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('overview'))

    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        flash("Logged in successfully")
        return redirect(url_for('overview'))
    return render_template('login.html', title='Login', form=form)


@tzundoku.route("/register", methods=['GET', 'POST'])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('overview'))
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('register.html', form=form)
        else:
            user = User(form.username.data, form.email.data, form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('You have created a new account')
            return redirect(url_for('overview')) 

    elif request.method == 'GET':
        return render_template('register.html', form=form)  

@tzundoku.route("/logout")
@login_required
def logout():
    logout_user() 
    return redirect(url_for('index')) 

@tzundoku.route("/overview", methods=['GET', 'POST'])
def overview():
    form = AddDokuForm()
    user = User.query.filter_by(id = current_user.id).first()

    titles = []
    doku = Doku.query.all()
    for a in doku:
        if a.parent == "Top":
            titles.append(a)
            for b in doku:
                if b.parent == a.title:
                    titles.append(b)
                    for c in doku:
                        if c.parent == b.title:
                            titles.append(c)


     
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('overview.html', titles=titles, form=form)
        else:
            doku = Doku(form.title.data, form.parent.data, user.id, datetime.datetime.utcnow())
            db.session.add(doku)
            db.session.commit()
            flash('You have created a new Doku!')
            return redirect(url_for('overview')) 

    elif request.method == 'GET':
        return render_template('overview.html', titles=titles, form=form)  

@tzundoku.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email= session['email']).first()  
    username = user.username
    return render_template('profile.html', username=username)

@tzundoku.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first()
    if user == None:
        flash('User not found.')
        return redirect(url_for('overview'))
    posts = Post.query.filter_by(user_id =id)
    return render_template('user.html',
                           user=user,
                           posts=posts)

@tzundoku.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It Works.'
    else:
        return 'Something is broken'

@tzundoku.route('/terms')
def terms():
    return render_template('legal.html',
                           title="Terms and Conditions",
                           content=legal.terms)
@tzundoku.route('/privacy')
def privacy():
    return render_template('legal.html',
                           title="Privacy Policy",
                           content=legal.privacy)

@tzundoku.route('/doku', methods=['GET', 'POST'])
def doku():
    user = User.query.filter_by(id = current_user.id).first()
    form = AddItemForm()
    dokuid = request.args['id']
    doku = Doku.query.filter_by(id = dokuid).first()
    header = doku.title
    items = Item.query.filter(Item.dokus.any(id = dokuid)).all()
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('doku.html', header=header, items=items, form=form, doku=doku)
        else:
            item = Item('music', form.title.data, form.artist.data, form.year.data, form.link.data, user.username, datetime.datetime.utcnow())
            item.dokus.append(doku)
            db.session.add(doku)
            db.session.add(item)
            db.session.commit()
            session['email'] = user.email
            flash('You have added an item')
            return redirect(url_for('doku', id=dokuid)) 

    elif request.method == 'GET':
        return render_template('doku.html', header=header, items=items, form=form, doku=doku)


@tzundoku.route('/item', methods=['GET', 'POST'])
def item():
    user = User.query.filter_by(id = current_user.id).first()
    form = AddPostForm()
    itemid = request.args['id']
    item = Item.query.filter_by(id = itemid).first()
    header = item.title
    posts = Post.query.filter_by(item_id = itemid)


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('item.html', header=header, posts=posts, form=form)
        else:
            post = Post(user.id, form.message.data, datetime.datetime.utcnow(), itemid)
            db.session.add(post)
            db.session.commit()
            flash('You have added a post!')
            return redirect(url_for('item', id=itemid)) 

    elif request.method == 'GET':
        return render_template('item.html', header=header, posts=posts, form=form)
    
@tzundoku.route('/makemoderator/<id>')
def makemoderator(id):
    user = User.query.filter_by(id=id).first()
    user.make_moderator() 
    flash('You have made this user a moderator')
    return redirect('overview')

@tzundoku.route('/removedoku/<id>')
@login_required
def removedoku(id):
    doku = Doku.query.filter_by(id=id).first()
    items = Item.query.filter(Item.dokus.any(id = doku.id)).all()
    for item in items:
        posts = Post.query.filter_by(item_id = id)
        for post in posts:
            post.delete()
        item.delete() 
    doku.delete()
    flash('You have removed this doku and its associated items and posts')
    return redirect('overview')

@tzundoku.route('/removeitem/<id>/<doku_id>')
@login_required
def delete(id, doku_id):
    item = Item.query.filter_by(id=id).first()
    posts = Post.query.filter_by(item_id = id)
    doku = Doku.query.filter_by(id=doku_id).first()
    #Problem!! Should remove just the doku page we are on

    doku_id = doku.id

    for post in posts:
        post.delete()
    item.delete()
    flash('You have removed this item and its associated posts!')
    return redirect(url_for('doku', id=doku_id))

@tzundoku.route('/removepost/<id>')
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first()
    item = Item.query.filter_by(id=post.item_id).first()
    item_id = item.id
    post.delete()
    flash('You have removed this post')
    return redirect(url_for('item', id=item_id))   


@tzundoku.route('/upvoteitem/<id>')
@login_required
def upvoteitem(id):
    item = Item.query.filter_by(id=id).first()
    item.upvoteitem()
    flash('You have upvoted this item')
    doku = Doku.query.filter_by(id=item.doku_id).first()
    doku_id = doku.id
    return redirect(url_for('doku', id=doku_id))

@tzundoku.route('/downvoteitem/<id>')
@login_required
def downvoteitem(id):
    item = Item.query.filter_by(id=id).first()
    item.downvoteitem()
    flash('You have downvoted this item')
    doku = Doku.query.filter_by(id=item.doku_id).first()
    doku_id = doku.id
    return redirect(url_for('doku', id=doku_id))

@tzundoku.route('/upvotepost/<id>')
@login_required
def upvotepost(id):
    post = Post.query.filter_by(id=id).first()
    post.upvotepost()
    flash('You have upvoted this post')
    item = Item.query.filter_by(id=post.item_id).first()
    item_id = item.id
    return redirect(url_for('item', id=item_id))

@tzundoku.route('/downvotepost/<id>')
@login_required
def downvotepost(id):
    post = Post.query.filter_by(id=id).first()
    post.downvotepost()
    flash('You have downvoted this post')
    item = Item.query.filter_by(id=post.item_id).first()
    item_id = item.id
    return redirect(url_for('item', id=item_id))


