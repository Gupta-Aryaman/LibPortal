from flask import Flask, Blueprint

from .extensions import init_db
from .views import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    init_db()

    app.register_blueprint(main)

    return app