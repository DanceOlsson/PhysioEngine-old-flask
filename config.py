import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    HEROKU = os.environ.get('HEROKU')
    
    # Use the HEROKU environment variable to determine if we're running on Heroku
    if HEROKU:
        BASE_URL = 'https://www.physioengine.com'  # Replace with your actual Heroku domain
    else:
        BASE_URL = 'http://localhost:8000'
    
    CSP = {
        'default-src': ["'self'", 'https:', 'data:'],
        'font-src': ["'self'", 'https:', 'data:'],
        'img-src': ["'self'", 'https:', 'data:'],
        'style-src': ["'self'", 'https:', "'unsafe-inline'"],
        'script-src': ["'self'", 'https:', "'unsafe-inline'", "'unsafe-eval'"]
    }