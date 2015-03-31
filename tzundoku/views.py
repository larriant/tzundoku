from flask import render_template, request, redirect, url_for, flash, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from tzundoku import tzundoku, db, lm
from .forms import LoginForm
from .forms import RegistrationForm
from .models import User

@tzundoku.route('/')
@tzundoku.route('/index')
def index():
    return render_template('index.html') 

@tzundoku.route("/login", methods=['GET', 'POST'])
def login(): 
    form = LoginForm() 
    if form.validate_on_submit():
        login_user(user)
        flash('Logged in successfully')
        return redirect('/overview')
    return render_template('login.html', title='Login', form=form)

@tzundoku.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@tzundoku.route("/logout")
def logout():
    return render_template('logout.html')

@tzundoku.route("/overview")
def overview():
    return render_template('overview.html')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
