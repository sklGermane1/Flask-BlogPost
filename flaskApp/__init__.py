
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config["SECRET_KEY"] = "ad8ce523989436fe2601582be3acdb5d"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from flaskApp import routes
