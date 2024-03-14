from flask import Flask, Blueprint

from .extensions import init_db, db_session
from .models import Librarian
from .views import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    init_db()

    # Create a librarian user
    librarian = Librarian(username='librarian', password='password')
    db_session.add(librarian)
    db_session.commit()

    app.register_blueprint(main)

    return app