# This file is the main entry point for the Flask application.
# It creates and configures the Flask app, initializes extensions,
# registers blueprints, and sets up context processors.

import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request
from flask_talisman import Talisman
from whitenoise import WhiteNoise
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/physioengine.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('PhysioEngine startup')

    # Register blueprints
    from app.routes import main, user, physio
    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(physio.bp, url_prefix='/physio')

    # Initialize extensions
    Talisman(app, content_security_policy=app.config['CSP'])
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')

    @app.after_request
    def add_security_headers(response):
        for header, value in app.config['SECURE_HEADERS'].items():
            response.headers[header] = value
        return response

    @app.before_request
    def log_request_info():
        app.logger.info('Headers: %s', request.headers)
        app.logger.info('Body: %s', request.get_data())

    return app