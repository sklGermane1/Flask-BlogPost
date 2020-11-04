from flask import Blueprint,render_template,request 
from flask_login import login_required
from flaskApp.models import Post
main = Blueprint("main",__name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get("page",1,type=int)
    posts = Post.query.paginate(page=page,per_page=5)
    return render_template("home.html", title="Home", posts=posts)


@main.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")

