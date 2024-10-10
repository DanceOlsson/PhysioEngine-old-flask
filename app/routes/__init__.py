from flask import Flask
from flask_talisman import Talisman
from whitenoise import WhiteNoise
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    Talisman(app, content_security_policy=app.config['CSP'], force_https=True)
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', prefix='static/')

    # Register blueprints
    from . import main, physio, user
    app.register_blueprint(main.bp)
    app.register_blueprint(physio.bp, url_prefix='/physio')
    app.register_blueprint(user.bp, url_prefix='/user')

    # Context Processor to inject current year into all templates
    @app.context_processor
    def inject_current_year():
        from datetime import datetime
        return {'current_year': datetime.now().year}

    return app