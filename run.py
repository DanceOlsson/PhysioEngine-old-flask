import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    port = int(os.environ.get('PORT', 8000))
    debug = env == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)