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
    

    #----------------------------------
    # Determine the BASE_URL This motherfucket is the reason it doesn't
    # work when scanning QR codes on a phone. It's something about  
    # the Heroku URL vs the ngrok URL.
    #----------------------------------
    # Determine the BASE_URL
    if os.environ.get('ENVIRONMENT') == 'production':
        BASE_URL = os.environ.get('BASE_URL') or 'https://www.physioengine.com'
    elif os.environ.get('USE_NGROK') == '1':
        BASE_URL = os.environ.get('NGROK_URL') or 'https://safe-newly-salmon.ngrok-free.app'
    else:
        BASE_URL = 'http://localhost:8000'
    
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
        SECURE_SSL_REDIRECT = True
    
    # Security headers
    SECURE_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    }
    
    # Add CSRF configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'your-csrf-secret-key'
