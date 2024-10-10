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
    
    # Check if the app is running on Heroku
    HEROKU = os.environ.get('HEROKU')
    
    # Set the BASE_URL depending on the environment (Heroku or local)
    if HEROKU:
        BASE_URL = 'https://www.physioengine.com'  # URL for Heroku deployment
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
    
    # Add these lines
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')