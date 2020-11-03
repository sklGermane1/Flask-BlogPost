from flask import Flask, render_template
from forms import RegisterForm, LoginForm, PostForm

app = Flask(__name__)

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
def home():
    return render_template("home.html", title="Home", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/post/<int:post_id>")
def get_post(post_id):
    pass


@app.route("/user/<string:username>")
def get_user(username):
    pass


@app.route("/account")
def account():
    pass


@app.route("/post")
def create_post():
    return render_template("post_form.html", title="Create Post", legend="Create Post")


@app.route("/post/<int:post_id>")
def update_post(post_id):
    return render_template("post_form.html", title="Create Post", legend="Create Post")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    pass


@app.route("/register")
def register():
    pass


@app.route("/login")
def login():
    pass


@app.route("/logout")
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)
