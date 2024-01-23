from flask import Blueprint
from .extensions import db_session
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def main_index():
    return 'Blueprint Views.py Hello!'

@main.route('/hello')
def main_hello():
    u = User('admin', 'admin@localhost')
    db_session.add(u)
    db_session.commit()
    return 'Success!'