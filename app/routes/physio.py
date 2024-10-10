from flask import Blueprint, render_template

bp = Blueprint('physio', __name__)

@bp.route('/')
def physio():
    return render_template('physio.html', show_navbar=True)

# Add other physio-related routes here if needed