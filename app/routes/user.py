from flask import Blueprint, render_template

bp = Blueprint('user', __name__)

@bp.route('/questionnaires')
def user_questionnaires():
    questionnaires = [
        {
            'name': 'Oswestry Disability Index',
            'slug': 'oswestry',
            'description': 'Assessing disability in patients with low back pain.'
        },
        # Add more questionnaires as needed
    ]
    return render_template('users/user_questionnaires.html', questionnaires=questionnaires, show_navbar=True)

# Add other user-related routes here if needed