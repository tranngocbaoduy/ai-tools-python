import os
import secrets
import requests

from PIL import Image
from flask import current_app,url_for 
from flask_mail import Message 
from io import BytesIO
from searchai import mail 
from searchai.models import User

def save_picture(url):
    # config place, name, size save picture
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex+'.png'
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
 
    img.thumbnail(output_size)

    img.save(picture_path, format='PNG')

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                 sender='noreply@demo.com',
                 recipients=[user.email])
                #  {'https://aitools-be.herokuapp.com/reset_password?token='+token}
    msg.body = f'''To reset your password, visit following link: 
                {'http://localhost:5000/reset_password?token='+token}
                If you did not make request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)

def check_token(token):
    # token = request.get_json()['token']  
    if verify_login(token):   
        return json.dumps(Respone(True, {}, "Authorized"))
    return json.dumps(Respone(False, {}, "Unauthorized"))

def verify_login(token):
    user = User.verify_login_token(token)   
    if user is None: 
        return False
    return True
