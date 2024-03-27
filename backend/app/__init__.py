from flask import Flask, Blueprint
from flask_cors import CORS

from .extensions import init_db, db_session
from .models import Librarian
from .views import main
from . import workers

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    
    celery = workers.celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND']
    )

    celery = workers.celery

    init_db()

    # Create a librarian user
    if not Librarian.query.filter_by(username='librarian').first():
        librarian = Librarian(username='librarian', password='password')
        db_session.add(librarian)
        db_session.commit()

    CORS(app)

    app.register_blueprint(main)

    return app, celery