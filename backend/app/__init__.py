from flask import Flask, Blueprint
from flask_cors import CORS
from flask_caching import Cache

from .extensions import init_db, db_session
from .models import Librarian
from .views import main

from . import workers
from .cache import cache


def create_app(config_file='settings.py'):
    app = Flask(__name__, template_folder="../templates")
    app.config.from_pyfile(config_file)

    cache.init_app(app)

    # Initialize database
    init_db()

    # Create a librarian user
    if not Librarian.query.filter_by(username='librarian').first():
        librarian = Librarian(username='librarian', password='password')
        db_session.add(librarian)
        db_session.commit()

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(main)

    celery = workers.celery
    celery.conf.update(
        broker_url = app.config['CELERY_BROKER_URL'],
        timezone="Asia/Kolkata",
        result_backend = app.config['CELERY_RESULT_BACKEND'],
    )

    celery.Task = workers.ContextTask
    app.app_context().push()
    
    return app, celery