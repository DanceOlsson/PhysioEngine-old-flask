# Import necessary modules
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define a Config class to store configuration settings
class Config:
    # Set the SECRET_KEY for Flask sessions and security
    # Use the value from environment variable if available, otherwise use a default
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Check if the app is running on Heroku and if HTTPS should be forced
    ON_HEROKU = os.environ.get('HEROKU', '0') == '1'
    FORCE_HTTPS = os.environ.get('FORCE_HTTPS', 'true').lower() == 'true'
    
    # Set the BASE_URL depending on the environment (Heroku or local)
    if ON_HEROKU:
        BASE_URL = 'https://www.physioengine.com'  # URL for Heroku deployment
        SERVER_NAME = os.environ.get('SERVER_NAME')
        PREFERRED_URL_SCHEME = 'https'
    else:
        BASE_URL = 'http://localhost:8000'  # URL for local development
    
    # Define Content Security Policy (CSP) settings
    # CSP helps prevent various types of attacks like XSS
    CSP = {
        'default-src': ["'self'", 'https:', 'data:'],  # Default source for content
        'font-src': ["'self'", 'https:', 'data:'],     # Allowed sources for fonts
        'img-src': ["'self'", 'https:', 'data:'],      # Allowed sources for images
        'style-src': ["'self'", 'https:', "'unsafe-inline'"],  # Allowed sources for styles
        'script-src': ["'self'", 'https:', "'unsafe-inline'", "'unsafe-eval'"]  # Allowed sources for scripts
    }
    
    # Debug and logging settings
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    # Configure SSL if necessary
    if ON_HEROKU and FORCE_HTTPS:
        # SSL configuration can be added here if needed
        pass
    
    # Security headers
    SECURE_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    }