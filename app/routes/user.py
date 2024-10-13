from flask import Blueprint, render_template, abort, request, current_app, url_for, redirect
from app.questionnaires_config import QUESTIONNAIRES
from app.utils.hoos_calculator import calculate_hoos_scores
from app.utils.koos_calculator import calculate_koos_scores
from app.routes.main import load_questionnaire_data
import logging

bp = Blueprint('user', __name__)

@bp.route('/questionnaires')
def user_questionnaires():
    return render_template('user_questionnaires.html', questionnaires=QUESTIONNAIRES, show_navbar=True)

@bp.route('/questionnaire/<string:questionnaire_slug>', methods=['GET', 'POST'])
def fill_questionnaire(questionnaire_slug):
    current_app.logger.info(f"Accessed fill_questionnaire with slug: {questionnaire_slug}, method: {request.method}")
    
    if questionnaire_slug not in QUESTIONNAIRES:
        current_app.logger.error(f"Invalid questionnaire slug: {questionnaire_slug}")
        abort(404)
    
    if request.method == 'POST':
        current_app.logger.info(f"POST request received for {questionnaire_slug}")
        current_app.logger.info(f"Form data: {request.form}")
        return handle_user_form_submission(questionnaire_slug)
    
    try:
        questionnaire_data = load_questionnaire_data(questionnaire_slug, 'swedish')
        if not questionnaire_data['sections']:
            current_app.logger.error(f"No sections found for {questionnaire_slug}")
            return "An error occurred while loading the questionnaire.", 500
        
        template = f'questionnaires/{questionnaire_slug}/{questionnaire_slug}_swe.html'
        form_action = url_for('user.fill_questionnaire', questionnaire_slug=questionnaire_slug)
        current_app.logger.info(f"Rendering template: {template} with form_action: {form_action}")
        
        return render_template(
            template,
            questionnaire_slug=questionnaire_slug,
            questionnaire_title=QUESTIONNAIRES[questionnaire_slug]['name'],
            instructions=questionnaire_data['instructions'],
            sections=questionnaire_data['sections'],
            evaluation_form=questionnaire_slug,
            form_action=form_action
        )
    except Exception as e:
        current_app.logger.error(f"Error in fill_questionnaire: {str(e)}", exc_info=True)
        return "An error occurred while loading the questionnaire.", 500

def handle_user_form_submission(questionnaire_slug):
    current_app.logger.info(f"Handling form submission for {questionnaire_slug}")
    try:
        responses = {key.split('_')[1]: int(value) for key, value in request.form.items() if key.startswith('question_')}
        current_app.logger.info(f"Received responses: {responses}")
        
        if questionnaire_slug == 'koos':
            result = calculate_koos_scores(responses)
        elif questionnaire_slug == 'hoos':
            result = calculate_hoos_scores(responses)
        else:
            current_app.logger.error(f"Unknown questionnaire type: {questionnaire_slug}")
            return "Unknown questionnaire type", 400
        
        current_app.logger.info(f"Calculated result: {result}")
        
        return render_template('display_result.html', result=result, show_navbar=True)
    except Exception as e:
        current_app.logger.error(f"Error in handle_user_form_submission: {str(e)}", exc_info=True)
        return "An error occurred while processing your responses.", 500