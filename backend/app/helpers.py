from functools import wraps
import jwt
from dotenv import load_dotenv
import os
from flask import request, make_response

from .models import User
from .extensions import db_session

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers['Authorization'])

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