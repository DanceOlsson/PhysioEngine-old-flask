"""
Configuration settings for the Flask application.

This module defines the Config class, which contains various configuration
settings for the Flask application, including security, database, and
environment-specific settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """
    Configuration class for the Flask application.

    This class contains various attributes that configure different aspects
    of the Flask application, such as security settings, database URIs,
    and environment-specific configurations.
    """

    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Check if the app is running on Heroku and if HTTPS should be forced
    ON_HEROKU = os.environ.get('HEROKU', '0') == '1'
    FORCE_HTTPS = os.environ.get('FORCE_HTTPS', 'true').lower() == 'true'
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # Determine the BASE_URL
    # This motherfucker is the reason it doesn't work when scanning QR codes on a phone.
    # It's something about the Heroku URL vs the ngrok URL.
    # DO NOT CHANGE THIS UNLESS YOU KNOW WHAT YOU ARE DOING.
    if os.environ.get('ENVIRONMENT') == 'production':
        BASE_URL = 'https://www.physioengine.com'
    elif os.environ.get('USE_NGROK') == '1':
        # Use the NGROK_URL from environment variables, or fall back to a default URL
        BASE_URL = os.environ.get('NGROK_URL') or 'https://safe-newly-salmon.ngrok-free.app'
    else:
        # Default to localhost for development environment
        BASE_URL = 'http://localhost:8000'
    
    # Security configurations
    PREFERRED_URL_SCHEME = 'https'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'your-csrf-secret-key'

    if ON_HEROKU and FORCE_HTTPS:
        # SSL configuration can be added here if needed
        SECURE_SSL_REDIRECT = True
    
    # Security headers to enhance application security
    SECURE_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    }
    
    # Define Content Security Policy (CSP) settings
    # CSP helps prevent various types of attacks like XSS
    CSP = {
        'default-src': "'self'",
        'style-src': [
            "'self'",
            'https://cdnjs.cloudflare.com',
            'https://fonts.googleapis.com',
            'https://cdn.jsdelivr.net',
        ],
        'script-src': [
            "'self'",
            'https://cdnjs.cloudflare.com',
            'https://cdn.jsdelivr.net',
        ],
        'font-src': [
            "'self'",
            'https://fonts.gstatic.com',
            'https://cdnjs.cloudflare.com',
        ],
        'img-src': [
            "'self'",
            'data:',
            'https://www.physioengine.com',
        ],
    }
