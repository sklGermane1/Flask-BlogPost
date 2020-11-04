from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length



class PostForm(FlaskForm):
    title = StringField("title", validators=[
        DataRequired(),
        Length(min=3)
    ])
    content = TextAreaField("content", validators=[
        DataRequired()
    ])


    submit = SubmitField("Create Post")