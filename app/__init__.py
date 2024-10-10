# This file is the main entry point for the Flask application.
# It creates and configures the Flask app, initializes extensions,
# registers blueprints, and sets up context processors.

from flask import Flask
from flask_talisman import Talisman
from whitenoise import WhiteNoise
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    return app