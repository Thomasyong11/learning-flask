from flask_wtf import Form
from wtforms import StringField, validators, PasswordField
from wtforms.fields.html5 import EmailField


class RegisterForm(Form):
    fullname = StringField("Full Name", [validators.DataRequired()])
    email = EmailField("Email Address", [validators.DataRequired(), validators.Email()])
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField("New Password", [validators.DataRequired(), validators.Length(min=4, max=80),
                                              validators.EqualTo("confirm", message="Password don't match")])
    confirm = PasswordField("Repeat Password")


class LoginForm(Form):
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField("Enter Password", [validators.DataRequired(), validators.Length(min=4, max=80)])
