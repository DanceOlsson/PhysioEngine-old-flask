from flask import Flask
from flask_talisman import Talisman
from whitenoise import WhiteNoise
from config import Config

def create_app(config_class=Config):
    """
    Create and configure an instance of the Flask application.

    Args:
        config_class (object): The configuration class to use. Defaults to Config.

    Returns:
        Flask: A configured Flask application instance.

    Raises:
        ImportError: If required modules are not found.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    # Talisman adds security headers and enables HTTPS
    Talisman(app, content_security_policy=app.config['CSP'], force_https=True)
    # WhiteNoise serves static files efficiently
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/', prefix='static/')

    # Register blueprints
    from . import main, physio, user
    app.register_blueprint(main.bp)
    app.register_blueprint(physio.bp, url_prefix='/physio')
    app.register_blueprint(user.bp, url_prefix='/user')

    @app.context_processor
    def inject_current_year():
        """
        Inject the current year into all templates.

        This function is automatically called for each request to add
        the current year to the template context.

        Returns:
            dict: A dictionary containing the current year.
        """
        from datetime import datetime
        return {'current_year': datetime.now().year}

    return app