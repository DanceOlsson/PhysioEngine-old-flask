from flask import Blueprint, render_template, request, redirect, url_for, current_app
import qrcode
import os
import uuid
import logging
import json
from urllib.parse import urljoin
from app.utils.koos_calculator import calculate_koos_scores  # Add this import
from app.questionnaires_config import QUESTIONNAIRES  # Add this import
from app.utils import calculate_koos_scores, calculate_hoos_scores

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html', show_navbar=True)

@bp.route('/generate_qr')
def generate_qr():
    evaluation_form = request.args.get('evaluation_form')
    if not evaluation_form:
        current_app.logger.warning("No evaluation form specified in the generate_qr request.")
        return "No evaluation form specified.", 400

    session_id = str(uuid.uuid4())
    base_url = current_app.config['BASE_URL']
    
    # Generate the relative URL
    relative_url = url_for('main.patient_form', session_id=session_id, evaluation_form=evaluation_form)
    
    # Join the base URL with the relative URL
    patient_form_url = urljoin(base_url, relative_url)

    current_app.logger.info(f"Generated QR code URL: {patient_form_url}")

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(patient_form_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    qr_directory = os.path.join('app', 'static', 'qr_codes')
    if not os.path.exists(qr_directory):
        os.makedirs(qr_directory)

    qr_filename = f"{session_id}.png"
    qr_path = os.path.join(qr_directory, qr_filename)
    img.save(qr_path)

    return redirect(url_for('main.wait_for_result', session_id=session_id, evaluation_form=evaluation_form))

@bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', show_navbar=False)

@bp.route('/test_env')
def test_env():
    heroku = current_app.config.get('HEROKU')
    base_url = current_app.config['BASE_URL']
    return f'HEROKU environment variable is set to: {heroku}<br>BASE_URL is: {base_url}'

@bp.route('/patient_form/<session_id>/<evaluation_form>', methods=['GET', 'POST'])
def patient_form(session_id, evaluation_form):
    logging.debug(f"Accessing patient_form with session_id: {session_id}, evaluation_form: {evaluation_form}")
    if request.method == 'POST':
        return handle_form_submission(session_id)
    else:
        return render_questionnaire(session_id, evaluation_form)

@bp.route('/wait_for_result/<session_id>/<evaluation_form>')
def wait_for_result(session_id, evaluation_form):
    result_file = os.path.join('results', f'{session_id}.json')
    if os.path.exists(result_file):
        try:
            return process_results(result_file, session_id, evaluation_form)
        except Exception as e:
            current_app.logger.error(f"Error processing results: {str(e)}", exc_info=True)
            return "An error occurred while processing your results.", 500
    else:
        return render_template('wait_for_result.html', session_id=session_id, evaluation_form=evaluation_form)

def handle_form_submission(session_id):
    try:
        responses = {key.split('_')[1]: int(value) for key, value in request.form.items() if key.startswith('question_')}
        
        result_directory = os.path.join('results')
        if not os.path.exists(result_directory):
            os.makedirs(result_directory)

        result_file = os.path.join(result_directory, f'{session_id}.json')

        with open(result_file, 'w') as file:
            json.dump(responses, file)
        current_app.logger.info(f"Saved responses to {result_file}")
        
        return redirect(url_for('main.thank_you'))
    except Exception as e:
        current_app.logger.error(f"Error saving responses: {str(e)}", exc_info=True)
        return "An error occurred while saving your responses.", 500

def render_questionnaire(session_id, evaluation_form):
    if evaluation_form not in ['koos', 'hoos']:
        logging.warning(f"Unknown evaluation form requested: {evaluation_form}")
        return "Form not found", 404

    try:
        data = load_questionnaire_data(evaluation_form, 'swedish')
        if not data['sections']:
            logging.error(f"No sections found for {evaluation_form}")
            return "An error occurred while loading the questionnaire.", 500
        
        return render_template(
            f'questionnaires/{evaluation_form}/{evaluation_form}_swe.html',
            session_id=session_id,
            questionnaire_slug=evaluation_form,
            questionnaire_title=QUESTIONNAIRES[evaluation_form]['name'],
            instructions=data.get('instructions', 'Instruktioner saknas.'),
            sections=data.get('sections', []),
            evaluation_form=evaluation_form,
            form_action=url_for('main.patient_form', session_id=session_id, evaluation_form=evaluation_form)
        )
    except Exception as e:
        logging.error(f"Error loading questionnaire data: {str(e)}")
        return "An error occurred while loading the questionnaire.", 500

def process_results(result_file, session_id, evaluation_form):
    try:
        with open(result_file, 'r') as file:
            responses = json.load(file)
        
        current_app.logger.info(f"Loaded responses: {responses}")
        
        if evaluation_form == 'koos':
            current_app.logger.info("Calculating KOOS scores")
            result = calculate_koos_scores(responses)
        elif evaluation_form == 'hoos':
            current_app.logger.info("Calculating HOOS scores")
            result = calculate_hoos_scores(responses)
        else:
            current_app.logger.error(f"Unknown questionnaire type: {evaluation_form}")
            return "Unknown questionnaire type", 400
        
        current_app.logger.info(f"Calculated result: {result}")
        
        if result is None:
            current_app.logger.error("Calculation returned None")
            return "Error in score calculation", 500

        os.remove(result_file)
        current_app.logger.info(f"Removed result file: {result_file}")
        
        qr_path = os.path.join('app', 'static', 'qr_codes', f'{session_id}.png')
        if os.path.exists(qr_path):
            os.remove(qr_path)
            current_app.logger.info(f"Removed QR code image: {qr_path}")
        
        return render_template('display_result.html', result=result)
    except Exception as e:
        current_app.logger.error(f"Error processing results: {str(e)}", exc_info=True)
        return "An error occurred while processing your results.", 500

def load_questionnaire_data(questionnaire, language='swedish'):
    filename = f'{questionnaire}_{language}.json'
    filepath = os.path.join('data', filename)
    logging.info(f"Attempting to load questionnaire data from: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if isinstance(data, list):
            data = data[0]
        
        instructions = data.get('instructions', 'Instruktioner saknas.')
        sections = data.get('sections', [])
        
        for section in sections:
            section['questions'] = [
                q if isinstance(q, dict) and 'id' in q
                else {'type': 'instructions', 'text': q['text']}
                for q in section.get('questions', [])
            ]
        
        return {"instructions": instructions, "sections": sections}
    except FileNotFoundError:
        logging.error(f"{questionnaire.upper()} data file not found: {filepath}")
        return {"instructions": "Instructions not available.", "sections": []}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON for {questionnaire}: {e}")
        return {"instructions": "Instructions not available.", "sections": []}
    except Exception as e:
        logging.error(f"Unexpected error loading {questionnaire} data: {str(e)}")
        return {"instructions": "Instructions not available.", "sections": []}
