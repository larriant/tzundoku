from flask import render_template, request, redirect, url_for, flash, session, json, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from tzundoku import tzundoku, db, lm
from .forms import LoginForm, RegistrationForm, AddDokuForm, AddItemForm, AddPostForm
from .models import User, Doku, Item, Post, Postvote, Itemvote, Dokuvote

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



@tzundoku.route("/overview", methods=['GET', 'POST'])
def overview():
    form = AddDokuForm()
    titles = []

    alldokus = Doku.query.all()
    parentlessdokus = []
    for a in alldokus: 
        titles.append(a)

    if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first()
        if form.validate() == False:
            return render_template('overview.html', titles=titles, form=form)
        else:
            doku_exists = Doku.query.filter_by(title=form.title.data).first()
            if doku_exists: #doku already eixsts
                newparent = Doku.query.filter_by(title=form.parent.data).first()
                if newparent == None: 
                    flash('This doku already exists') 
                    return redirect(url_for('overview'))
                else: 
                    newparent.children.append(doku_exists)
                    db.session.add(newparent)
                    db.session.add(doku_exists)
                    db.session.commit()
                    flash('This doku already exists, but you have added a parent!')
                    return redirect(url_for('overview')) 

            else: #dok does not yet exist 
                newparent = Doku.query.filter_by(title=form.parent.data).first()
                if newparent == None:
                    doku_no_parent = Doku(form.title.data, user.id, datetime.datetime.utcnow())
                    db.session.add(doku_no_parent)
                    db.session.commit()
                    flash('You have created a new Doku, with no parent!')
                    return redirect(url_for('overview')) 
                else: 
                    doku_with_parent = Doku(form.title.data, user.id, datetime.datetime.utcnow())
                    newparent.children.append(doku_with_parent)
                    db.session.add(newparent)
                    db.session.add(doku_with_parent)
                    db.session.commit()
                    flash('You have created a new Doku, with a new parent')
                    return redirect(url_for('overview'))
                
    elif request.method == 'GET':
        return render_template('overview.html', titles=titles, form=form)  

@tzundoku.route('/doku', methods=['GET', 'POST'])
def doku():
    form = AddItemForm()
    dokuid = request.args['id']
    doku = Doku.query.filter_by(id = dokuid).first()
    showitems = doku.showitems()
    header = doku.title
    items = Item.query.filter(Item.dokus.any(id = dokuid)).all()
    items2 = []
    for a in doku.children:
        if a == doku:
            continue
        else:
            items2.append(Item.query.filter(Item.dokus.any(id= a.id)).all())

    if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first()
        if form.validate() == False:
            return render_template('doku.html', header=header, items=items, items2=items2, form=form, doku=doku, showitems=showitems)
        else:
            item_exists = Item.query.filter_by(title = form.title.data).first()
            if item_exists:
                item_exists.dokus.append(doku)
                db.session.add(item_exists)
                db.session.add(doku)
                db.session.commit() 
                flash('You have added an item that already exists to this doku')
                return redirect(url_for('doku', id=dokuid))
            else:
                item = Item('music', form.title.data, form.artist.data, form.year.data, form.link.data, form.imglink.data, user.username, datetime.datetime.utcnow())
                item.dokus.append(doku)
                db.session.add(doku)
                db.session.add(item)
                db.session.commit()
                session['email'] = user.email
                flash('You have added an item')
                return redirect(url_for('doku', id=dokuid)) 

    elif request.method == 'GET':
        return render_template('doku.html', header=header, items=items, items2=items2, form=form, doku=doku, showitems=showitems)


@tzundoku.route('/item', methods=['GET', 'POST'])
def item(): 
    form = AddPostForm()
    itemid = request.args['id']
    item = Item.query.filter_by(id = itemid).first()

    if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first() 
        if form.validate() == False:
            return render_template('item.html', item=item, form=form)
        else:
            post = Post(user.id, form.message.data, datetime.datetime.utcnow(), itemid)
            db.session.add(post)
            db.session.commit()
            flash('You have added a post!')
            return redirect(url_for('item', id=itemid)) 

    elif request.method == 'GET':
        return render_template('item.html', item=item, form=form)
    
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
def removeitem(id, doku_id):
    item = Item.query.filter_by(id=id).first()
    posts = Post.query.filter_by(item_id = id)
    doku = Doku.query.filter_by(id=doku_id).first()

    doku_id = doku.id
    for post in posts:
        post.delete()
    item.delete()
    flash('You have removed this item and its associated posts!')
    return redirect(url_for('doku', id=doku_id))

@tzundoku.route('/removepost/<id>')
@login_required
def removepost(id):
    post = Post.query.filter_by(id=id).first()
    item = Item.query.filter_by(id=post.item_id).first()
    item_id = item.id
    post.delete()
    flash('You have removed this post')
    return redirect(url_for('item', id=item_id))   

@tzundoku.route('/upvotepost', methods=["POST"])
@login_required
def upvotepost():
    if request.method == "POST":  
        post = Post.query.filter_by(id = request.json['post_id']).first()
        postvote = Postvote.query.filter_by(post_id = request.json['post_id']).filter_by(user_id= request.json['user_id']).first()
        if postvote:
            if postvote.vote == True:
                db.session.delete(postvote)
                db.session.commit()
            elif postvote.vote == False:
                db.session.delete(postvote)
                newpostvote = Postvote(request.json['user_id'], request.json['post_id'], request.json['vote'])
                db.session.add(newpostvote)
                db.session.commit()
        else:
            newpostvote = Postvote(request.json['user_id'], request.json['post_id'], request.json['vote'])
            db.session.add(newpostvote)
            db.session.commit()
        votes = post.numvotes()
        return jsonify({'numvotes': votes, 'post_id': post.id})

@tzundoku.route('/downvotepost', methods=["POST"])
@login_required
def downvotepost():
    if request.method == "POST":  
        post = Post.query.filter_by(id = request.json['post_id']).first()
        postvote = Postvote.query.filter_by(post_id = request.json['post_id']).filter_by(user_id= request.json['user_id']).first()
        if postvote:
            if postvote.vote == False:
                db.session.delete(postvote)
                db.session.commit()
            elif postvote.vote == True:
                db.session.delete(postvote)
                newpostvote = Postvote(request.json['user_id'], request.json['post_id'], request.json['vote'])
                db.session.add(newpostvote)
                db.session.commit()
        else:
            newpostvote = Postvote(request.json['user_id'], request.json['post_id'], request.json['vote'])
            db.session.add(newpostvote)
            db.session.commit()
        votes = post.numvotes()
        return jsonify({'numvotes': votes, 'post_id': post.id})

@tzundoku.route('/upvoteitem', methods=["POST"])
@login_required
def upvoteitem():
    if request.method == "POST":  
        item = Item.query.filter_by(id = request.json['item_id']).first()
        itemvote = Itemvote.query.filter_by(item_id= request.json['item_id']).filter_by(user_id= request.json['user_id']).filter_by(doku_id = request.json['doku_id']).first()
        if itemvote:
            if itemvote.vote == True:
                db.session.delete(itemvote)
                db.session.commit()
            elif itemvote.vote == False:
                db.session.delete(itemvote)
                newitemvote = Itemvote(request.json['user_id'], request.json['item_id'], request.json['doku_id'], request.json['vote'])
                db.session.add(newitemvote)
                db.session.commit()
        else:
            newitemvote = Itemvote(request.json['user_id'], request.json['item_id'], request.json['doku_id'], request.json['vote'])
            db.session.add(newitemvote)
            db.session.commit()
        votes = item.numvotes(request.json['doku_id'])
        return jsonify({'numvotes': votes, 'item_id': item.id})

@tzundoku.route('/downvoteitem', methods=["POST"])
@login_required
def downvoteitem():
    if request.method == "POST":  
        item = Item.query.filter_by(id = request.json['item_id']).first()
        itemvote = Itemvote.query.filter_by(item_id = request.json['item_id']).filter_by(user_id= request.json['user_id']).filter_by(doku_id = request.json['doku_id']).first()
        if itemvote:
            if itemvote.vote == False:
                db.session.delete(itemvote)
                db.session.commit()
            elif itemvote.vote == True:
                db.session.delete(itemvote)
                newitemvote = Itemvote(request.json['user_id'], request.json['item_id'], request.json['doku_id'],  request.json['vote'])
                db.session.add(newitemvote)
                db.session.commit()
        else:
            newitemvote = Itemvote(request.json['user_id'], request.json['item_id'], request.json['doku_id'], request.json['vote'])
            db.session.add(newitemvote)
            db.session.commit()
        votes = item.numvotes(request.json['doku_id'])
        return jsonify({'numvotes': votes, 'item_id': item.id})

