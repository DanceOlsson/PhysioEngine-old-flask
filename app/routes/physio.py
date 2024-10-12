from flask import Blueprint, render_template
from app.questionnaires_config import QUESTIONNAIRES

bp = Blueprint('physio', __name__)

@bp.route('/')
def physio():
    return render_template('physio.html', questionnaires=QUESTIONNAIRES, show_navbar=True)

# Add other physio-related routes here if needed