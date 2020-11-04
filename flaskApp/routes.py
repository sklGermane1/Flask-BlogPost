from flaskApp import app, db, bcrypt
from flask import render_template, flash, redirect, url_for,request
from flaskApp.forms import RegisterForm, LoginForm, PostForm,UpdateUserForm
from flaskApp.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from PIL import Image
import os
posts = [
    {
        id: "1",
        "title": "title of my Post",
        "content": "content of my Post",
    },
    {
        id: "2",
        "title": "title of my scnd Post",
        "content": "content of my scnd Post",
    },
    {
        id: "3",
        "title": "title of my 3 Post",
        "content": "content of my 3 Post",
    },
]


# Routes


@app.route("/")
@app.route("/home")
@login_required
def home():
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


@app.route("/post/<int:post_id>")
@login_required
def update_post(post_id):
    return render_template("post_form.html", title="Create Post", legend="Create Post")


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    pass


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
