from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = TextField('username', [validators.required()]) 
    password = PasswordField('password', [validators.required()])


class RegistrationForm(Form):
    username = TextField('username', [validators.Length(min=4, max=10)])
    email = TextField('email', [validators.Length(min=6, max=15)])
    password = PasswordField('password', [validators.required(), validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('confirmpassword')
