from flask import Blueprint, request, make_response
from .extensions import db_session
from .models import *
import jwt
import datetime
from dotenv import load_dotenv
import os
from .helpers import token_required

load_dotenv()

main = Blueprint('main', __name__)
secret_key = os.getenv('SECRET_KEY')


@main.route('/signup', methods = ["POST"])
def signup_user():
    '''
    Signup endpoint for a student (user)
    '''
    if request.method == "POST":
        try:
            username = request.json["username"]
            email = request.json['email']
            password = request.json['password']

            fetch_existing_email = db_session.query(User).filter(User.email == email).all()

            if fetch_existing_email:
                return make_response({"Status": "email already exists"}, 403)

            u = User(username, email, password)
            db_session.add(u)
            db_session.commit()

            return make_response({"Status": "User added succesfully"}, 200)
        
        except Exception as e:
            return make_response({'Error: ': str(e)}, 500)
    
    return make_response({"Status": 'Internal Server Error!'}, 500)


@main.route('/login', methods = ["POST"])
def login_user():
    '''
    Login endpoint for a student (user)
    '''
    if request.method == "POST":
        try:
            email = request.json['email']
            password = request.json['password']

            fetch_user = db_session.query(User).filter(User.email == email and User.check_password(password)).all()

            if not fetch_user:
                return make_response({"Status": "Invalid Credentials"}, 401)

            fetch_user = fetch_user[0]
            token = jwt.encode({'username': fetch_user.username, 'email': fetch_user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)

            return make_response({"Status": "User login successful", "token": token}, 200)
        
        except Exception as e:
            return make_response({'Error: ': str(e)}, 500)
        
    return make_response({"Status": 'Internal Server Error!'}, 500)


# search a book by title
# see all books

# borrow a book
# return a book
# see all borrowed books
# see all returned books
# see all books in a section

@main.route('/protected', methods = ["GET"])
@token_required
def protected(current_user):
    return make_response({'message': 'This is only available for people with valid tokens'}, 200)