from flask import Blueprint,render_template,redirect,url_for,request,flash,abort
from flask_login import login_required,current_user
from flaskApp import db,app,mail,bcrypt
from flaskApp.models import Post 
from flaskApp.posts.forms import PostForm
posts = Blueprint("posts",__name__)


@posts.route("/post/<int:post_id>")
@login_required
def get_post(post_id):
    pass







@posts.route("/post",methods=["GET","POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("You successfully created an Post","success")
        return redirect(url_for("main.home"))
    return render_template("post_form.html", title="Create Post", legend="Create Post",form=form)


@posts.route("/post/<int:post_id>/update",methods=["GET","POST"])
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
        return redirect(url_for("main.home"))
    elif request.method ==  "GET":
        form.title.data = post.title   
        form.content.data = post.content
    return render_template("post_form.html", title="Update Post", legend="Update Post",form=form)


@posts.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been deleted!","success")
    return redirect(url_for("main.home"))



