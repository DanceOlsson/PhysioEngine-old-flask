# This file is the main entry point for the Flask application.
# It creates and configures the Flask app, initializes extensions,
# registers blueprints, and sets up context processors.

from flask import Flask
from flask_talisman import Talisman
from whitenoise import WhiteNoise
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from app.routes import main, user, physio
    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(physio.bp, url_prefix='/physio')

    # Initialize extensions
    Talisman(app)
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')

    return app