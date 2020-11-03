from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, PasswordField, StringField
from wtforms.validators import Length, Email, DataRequired, EqualTo

# POST


class PostForm(FlaskForm):
    title = StringField("title", validators=[
        DataRequired(),
        Length(min=3)
    ])
    content = TextAreaField("content", validators=[
        DataRequired()
    ])
# AUTH


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=3, max=10)
    ])
    email = StringField("email", validators=[
        DataRequired(),
        Length(min=4),
        Email()
    ])
    password = PasswordField("password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField("confirm password", validators=[
        DataRequired(),
        Length(min=6),
        EqualTo("password")
    ])

    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=3, max=10)
    ])
    password = PasswordField("password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    remember = BooleanField("Remember me")

    submit = SubmitField("Login")
