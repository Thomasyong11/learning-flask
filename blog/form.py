from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, PasswordField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from blog.models import Category


class SetupForm(Form):
    name = StringField("Blog Name", [validators.DataRequired(), validators.Length(max=80)])
    fullname = StringField("Full Name", [validators.DataRequired()])
    email = EmailField("Email Address", [validators.DataRequired(), validators.Email()])
    username = StringField("Username", [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField("New Password", [validators.DataRequired(), validators.Length(min=4, max=80),
                                              validators.EqualTo("confirm", message="Password don't match")])
    confirm = PasswordField("Repeat Password")


def categories():
    return Category.query


class PostForm(Form):
    image = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'gif'], "Images Only!")])
    title = StringField("Title", [validators.DataRequired(), validators.Length(min=5, max=50)])
    body = TextAreaField("Content", [validators.DataRequired()])
    category = QuerySelectField("Category", query_factory=categories, allow_blank=True)
    new_category = StringField("New Category")