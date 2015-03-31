from flask import render_template, request, redirect, url_for, flash
from tzundoku import tzundoku 
from .forms import LoginForm
from .forms import RegistrationForm

@tzundoku.route('/')
@tzundoku.route('/index')
def index():
    return render_template('index.html') 

@tzundoku.route("/login", methods=['GET', 'POST'])
def login(): 
    form = LoginForm() 
    if form.validate_on_submit():
        flash('Login requested for Username="%s", Password=%s' % (form.username, form.password))
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


