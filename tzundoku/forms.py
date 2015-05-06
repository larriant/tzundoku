from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField, SubmitField, SelectField, TextAreaField
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
    email = TextField('email', [validators.required("Please enter an email"), validators.Email("Please enter an email"), validators.Length(min=6, max=35, message="Please enter an email between 6 and 35 characters long")])
    password = PasswordField('password', [validators.required("Please enter a password"), validators.EqualTo('confirm', message = 'Passwords must match'), validators.Length(min=6, max=25, message="Please enter a password between 6 and 25 characters long")])
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
        
        user2 = User.query.filter_by(username = self.username.data.lower()).first()
        if user2:
            self.username.errors.append("That username is already taken")
            return False 

        else:
            return True


class AddDokuForm(Form):
    title = TextField('title', [validators.required("Please enter a title")])
    parent = SelectField('parent')
    submit = SubmitField('Add Doku')


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class AddItemForm(Form):
    itemtype = SelectField('itemtype', choices= [('', 'What type of item?'),('album','Album'), ('film','Film'), ('book', 'Book'), ( 'article', 'Article')])
    title = TextField('title', [validators.required("Please enter a title")])
    artist = TextField('artist')
    year = TextField('year', [validators.required("Please enter a year!")])
    link = TextField('link')
    imglink = TextField('imglink')
    submit = SubmitField('Add Item')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        
        if self.itemtype.data == 'album':
            if self.artist.data == '':
                return False
            else:
                return True

class AddPostForm(Form):
    message = TextAreaField('message', [validators.required()])
    submit = SubmitField('Add Post')
    
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class EditPostForm(Form):
    message = TextAreaField('message', [validators.required()])
    submit = SubmitField('Edit Post')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class EditItemForm(Form):
    link = TextField('link', [validators.required()])
    imglink = TextField('imglink',[validators.required()])
    submit = SubmitField('Edit Item')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
