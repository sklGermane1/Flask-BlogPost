from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, PasswordField, StringField
from wtforms.validators import Length, Email, DataRequired, EqualTo,ValidationError
from flask_login import current_user
from flaskApp.models import User
from flask_wtf.file import FileField,FileAllowed
# POST


class PostForm(FlaskForm):
    title = StringField("title", validators=[
        DataRequired(),
        Length(min=3)
    ])
    content = TextAreaField("content", validators=[
        DataRequired()
    ])


    submit = SubmitField("Create Post")
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

    def validate_username(self,username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists")

    def validate_email(self,email):
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists")


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

class UpdateUserForm(FlaskForm):
    username = StringField("username", validators=[
        DataRequired(),
        Length(min=3, max=10)
    ])
    email = StringField("email", validators=[
        DataRequired(),
        Length(min=3)
    ])
    picture = FileField("Update Profile Picture",validators=[
        FileAllowed("jpg","png")
        ])
    submit = SubmitField("Update")  

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists")

    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists")


    
