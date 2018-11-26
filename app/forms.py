from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import validators

class ContactForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Wyslij do puc', validators=[DataRequired()])


#Article Class Form
class ArticleForm(FlaskForm):
    id = IntegerField('id', [validators.length(min=1)])
    title = StringField('title', [validators.length(min=1, max=200)])
    content = TextAreaField('content', [validators.length(min=30)])