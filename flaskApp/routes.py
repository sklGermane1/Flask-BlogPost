from flaskApp import app, db, bcrypt,mail
from flask import render_template, flash, redirect, url_for,request,abort
from flaskApp.forms import RegisterForm, LoginForm, PostForm,UpdateUserForm,Request_reset_form,Reset_password_form
from flaskApp.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from PIL import Image
from flask_mail import Message
import os

# Routes


@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get("page",1,type=int)
    posts = Post.query.paginate(page=page,per_page=5)
    return render_template("home.html", title="Home", posts=posts)


@app.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")


@app.route("/post/<int:post_id>")
@login_required
def get_post(post_id):
    pass


@app.route("/user/<string:username>")
@login_required
def get_user(username):
    pass


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
    sender="billcrafter007@gmail.com",
    recipients=[user.email])
    msg.body = f""" 
    To reset your password, visit the following link:
    {url_for('reset_password_request',token=token,_external=True)}
    """

    mail.send(msg)
    

@app.route("/reset_password",methods=["GET","POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Request_reset_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sended to this email address","info")
        return redirect(url_for('login'))
    return render_template("request_password.html",form=form,title="Reset Password")


@app.route("/reset_password/<token>",methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid/Expired token","danger")
        return redirect(url_for('reset_password_request'))
    form = Reset_password_form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been changed!","success")
        return redirect(url_for('login'))
    return render_template("reset_token.html",title="Reset Password",form=form)


def save_file(image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.join(image.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,"static/profile_pics",picture_fn)

    output_size = (125,125)
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account",methods=["GET","POST"])
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
        return redirect(url_for("home")) 
        
    elif request.method == "GET":
            form.username.data = current_user.username 
            form.email.data = current_user.email 
    image_file = url_for("static",filename="profile_pics/" + current_user.image_file)
    return render_template("account.html",title="Account",form=form,image_file=image_file)


@app.route("/post",methods=["GET","POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You successfully created an Post","success")
        return redirect(url_for("home"))
    return render_template("post_form.html", title="Create Post", legend="Create Post",form=form)


@app.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data   
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been updated!","success")
        return redirect(url_for("home"))
    elif request.method ==  "GET":
        form.title.data = post.title   
        form.content.data = post.content
    return render_template("post_form.html", title="Update Post", legend="Update Post",form=form)


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been deleted!","success")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You are now Registered!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Wrong Credentials","danger")
    return render_template("login.html",title="Login",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
