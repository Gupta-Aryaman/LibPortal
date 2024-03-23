from flask import Flask, Blueprint
from flask_cors import CORS

from .extensions import init_db, db_session
from .models import Librarian
from .views import main


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    init_db()

    # Create a librarian user
    if not Librarian.query.filter_by(username='librarian').first():
        librarian = Librarian(username='librarian', password='password')
        db_session.add(librarian)
        db_session.commit()

    CORS(app)

    app.register_blueprint(main)

    return app