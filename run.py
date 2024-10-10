import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True, port=port)
    else:
        app.run(host='0.0.0.0', port=port)