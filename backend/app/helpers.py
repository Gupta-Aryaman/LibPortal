from functools import wraps
import jwt
from dotenv import load_dotenv
import os
from flask import request, make_response

from .models import User
from .extensions import db_session

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return make_response({'Message': 'a valid token is missing'}, 401)

        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = db_session.query(User).filter(User.email == data['email']).first()
        except Exception as e:
            return make_response({'message': str(e)}, 401)

        return f(current_user, *args, **kwargs)

    return decorated


def librarian_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return make_response({'Message': 'a valid token is missing'}, 401)

        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            current_user = db_session.query(User).filter(User.email == data['username'], User.role == 'librarian').first()
        except Exception as e:
            return make_response({'message': str(e)}, 401)

        return f(current_user, *args, **kwargs)

    return decorated


import os, smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.application import MIMEApplication

def send_email(address, subject, message, attachment=None, filename=None, subtype=None):
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_EMAIL = "librarian@eLibrary.com"
    SENDER_PASSWORD = ""

    msg = MIMEMultipart('alternative')
    msg["From"] = SENDER_EMAIL
    msg["To"] = address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    if attachment:
        part = MIMEApplication(attachment.read(), _subtype=subtype)
        part.add_header("Content-Disposition", "attachment", filename= filename)
        msg.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_EMAIL, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()