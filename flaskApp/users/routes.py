from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import current_user,login_user,logout_user,login_required
from flaskApp import db,bcrypt
from flaskApp.users.forms import RegisterForm,LoginForm,Request_reset_form,Reset_password_form,UpdateUserForm
from flaskApp.models import User
from flaskApp.users.utils import save_file,send_reset_email
users = Blueprint("users",__name__)



@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You are now Registered!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Wrong Credentials","danger")
    return render_template("login.html",title="Login",form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account",methods=["GET","POST"])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_file(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data   
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated","success")
        return redirect(url_for("main.home")) 
        
    elif request.method == "GET":
            form.username.data = current_user.username 
            form.email.data = current_user.email 
    image_file = url_for("static",filename="profile_pics/" + current_user.image_file)
    return render_template("account.html",title="Account",form=form,image_file=image_file)

@users.route("/user/<string:username>")
@login_required
def get_user(username):
    pass



@users.route("/reset_password",methods=["GET","POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = Request_reset_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sended to this email address","info")
        return redirect(url_for('users.login'))
    return render_template("request_password.html",form=form,title="Reset Password")


@users.route("/reset_password/<token>",methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid/Expired token","danger")
        return redirect(url_for('users.reset_password_request'))
    form = Reset_password_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been changed!","success")
        return redirect(url_for('users.login'))
    return render_template("reset_token.html",title="Reset Password",form=form)


