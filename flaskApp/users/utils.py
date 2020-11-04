import secrets 
import os 
from flask import url_for
from flaskApp import app,mail 
from flask_mail import Message
from PIL import Image
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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
    sender="billcrafter007@gmail.com",
    recipients=[user.email])
    msg.body = f""" 
    To reset your password, visit the following link:
    {url_for('users.reset_password_request',token=token,_external=True)}
    """

    mail.send(msg)
    
