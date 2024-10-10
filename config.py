import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')
    HEROKU = os.environ.get('HEROKU')
    CSP = {
        'default-src': ["'self'", 'https:', 'data:'],
        'font-src': ["'self'", 'https:', 'data:'],
        'img-src': ["'self'", 'https:', 'data:'],
        'style-src': ["'self'", 'https:', "'unsafe-inline'"],
        'script-src': ["'self'", 'https:', "'unsafe-inline'", "'unsafe-eval'"]
    }