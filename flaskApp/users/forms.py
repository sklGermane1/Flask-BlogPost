from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskApp.models import User
from flask_login import current_user


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



class Request_reset_form(FlaskForm):
    email = StringField("email",validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField("Send Email")

    
class Reset_password_form(FlaskForm):
    password = PasswordField("password", validators=[
    DataRequired(),
    Length(min=6)
    ])
    confirm_password = PasswordField("confirm password", validators=[
        DataRequired(),
        Length(min=6),
        EqualTo("password")
    ])

    submit = SubmitField("Reset Password")