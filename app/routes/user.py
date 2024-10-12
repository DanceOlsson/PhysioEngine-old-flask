from flask import Blueprint, render_template, abort, request, current_app, url_for, redirect, jsonify
from app.questionnaires_config import QUESTIONNAIRES
from app.utils.hoos_calculator import calculate_hoos_scores
from app.utils.koos_calculator import calculate_koos_scores
from app.routes.main import load_questionnaire_data  # Import the function from main.py

bp = Blueprint('user', __name__)

@bp.route('/questionnaires')
def user_questionnaires():
    # Render the user_questionnaires template with the list of available questionnaires
    # The show_navbar parameter is set to True to display the navigation bar
    return render_template('users/user_questionnaires.html', questionnaires=QUESTIONNAIRES, show_navbar=True)

@bp.route('/questionnaire/<string:questionnaire_slug>', methods=['GET', 'POST'])
def fill_questionnaire(questionnaire_slug):
    if questionnaire_slug not in QUESTIONNAIRES:
        abort(404)
    
    if request.method == 'POST':
        return handle_user_form_submission(questionnaire_slug)
    
    try:
        questionnaire_data = load_questionnaire_data(questionnaire_slug, 'swedish')
        if not questionnaire_data['sections']:
            current_app.logger.error(f"No sections found for {questionnaire_slug}")
            return "An error occurred while loading the questionnaire.", 500
        
        template = f'questionnaires/{questionnaire_slug}/{questionnaire_slug}_swe.html'
        return render_template(
            template,
            questionnaire_slug=questionnaire_slug,
            instructions=questionnaire_data['instructions'],
            sections=questionnaire_data['sections']
        )
    except Exception as e:
        current_app.logger.error(f"Error loading questionnaire data: {str(e)}")
        return "An error occurred while loading the questionnaire.", 500

def handle_user_form_submission(questionnaire_slug):
    try:
        responses = {key.split('_')[1]: int(value) for key, value in request.form.items() if key.startswith('question_')}
        
        if questionnaire_slug == 'hoos':
            result = calculate_hoos_scores(responses)
        elif questionnaire_slug == 'koos':
            result = calculate_koos_scores(responses)
        else:
            abort(400, description="Unsupported questionnaire type")
        
        return render_template('display_result.html', result=result)
    except Exception as e:
        current_app.logger.error(f"Error processing user form submission: {str(e)}", exc_info=True)
        return "An error occurred while processing your responses.", 500
