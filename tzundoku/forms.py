from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField, SubmitField, SelectField
from .models import User

class LoginForm(Form):
    username = TextField('username', [validators.required("Please enter a Username")]) 
    password = PasswordField('password', [validators.required("Please enter a Password")])
    submit = SubmitField("Login")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username= self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid e-mail or password")
            return False

class RegistrationForm(Form):
    username = TextField('username', [validators.required("Please enter a Username"), validators.Length(min=4, max=20)])
    email = TextField('email', [validators.required("Please enter an email"), validators.Email("Please enter an email"), validators.Length(min=6, max=35)])
    password = PasswordField('password', [validators.required(), validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('confirmpassword', [validators.required("Please enter a Password")])
    submit = SubmitField("Register")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class AddDokuForm(Form):
    title = TextField('title', [validators.required("Please enter a title")])
    parent = TextField('parent', [validators.required("Please enter the parent")]) 
    submit = SubmitField('Add Doku')


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class AddItemForm(Form):
    title = TextField('title', [validators.required()])
    artist = TextField('artist', [validators.required()])
    year = TextField('year', [validators.required()])
    link = TextField('link', [validators.required()])
    submit = SubmitField('Add Item')
    
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class AddPostForm(Form):
    message = TextField('message', [validators.required()])
    submit = SubmitField('Add Post')
    
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)



